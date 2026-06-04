const CONFIG = {
  evaluationSheet: 'Evaluations',
  dashboardSheet: 'QA Dashboard',
  guideSheet: 'Category Guide',
  lowConfidenceThreshold: 0.70,
  headers: [
    'record_id',
    'product_description',
    'brand',
    'ai_predicted_category',
    'ai_confidence',
    'reviewer_approved_category',
    'error_reason',
    'review_status',
    'reviewer_notes',
    'category_match',
    'priority',
    'reviewed_at'
  ]
};

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('AI QA Tools')
    .addItem('Set up workbook', 'setupWorkbook')
    .addItem('Recalculate QA flags', 'recalculateAllRows')
    .addItem('Refresh QA dashboard', 'refreshDashboard')
    .addItem('Assign next review item', 'assignNextReviewItem')
    .addToUi();
}

function setupWorkbook() {
  const spreadsheet = SpreadsheetApp.getActive();
  const evaluations = getOrCreateSheetFromAliases_(
    spreadsheet,
    CONFIG.evaluationSheet,
    ['sample_product_evaluations']
  );
  const dashboard = getOrCreateSheet_(spreadsheet, CONFIG.dashboardSheet);
  const guide = getOrCreateSheetFromAliases_(
    spreadsheet,
    CONFIG.guideSheet,
    ['category_guide']
  );

  if (evaluations.getLastRow() === 0) {
    evaluations.getRange(1, 1, 1, CONFIG.headers.length).setValues([CONFIG.headers]);
  } else {
    ensureEvaluationColumns_(evaluations);
  }

  formatEvaluationSheet_(evaluations);
  formatGuideSheet_(guide);
  refreshDashboard();
  spreadsheet.setActiveSheet(evaluations);
  SpreadsheetApp.getUi().alert(
    'Workbook ready',
    'The required tabs are ready. Use AI QA Tools > Recalculate QA flags, then refresh the QA dashboard.',
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

function onEdit(event) {
  if (!event || !event.range) return;
  const sheet = event.range.getSheet();
  if (sheet.getName() !== CONFIG.evaluationSheet || event.range.getRow() === 1) return;

  ensureEvaluationColumns_(sheet);
  evaluateRow_(sheet, event.range.getRow());
}

function recalculateAllRows() {
  const sheet = SpreadsheetApp.getActive().getSheetByName(CONFIG.evaluationSheet);
  if (!sheet || sheet.getLastRow() < 2) return;

  ensureEvaluationColumns_(sheet);
  for (let row = 2; row <= sheet.getLastRow(); row++) {
    evaluateRow_(sheet, row);
  }
  refreshDashboard();
}

function evaluateRow_(sheet, row) {
  const headerMap = getHeaderMap_(sheet);
  const values = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];
  const predicted = String(values[headerMap.ai_predicted_category] || '').trim();
  const approved = String(values[headerMap.reviewer_approved_category] || '').trim();
  const confidence = Number(values[headerMap.ai_confidence]);
  const status = String(values[headerMap.review_status] || '').trim();
  const errorReason = String(values[headerMap.error_reason] || '').trim();

  let match = 'Pending Review';
  if (approved) match = predicted === approved ? 'Match' : 'Mismatch';

  let priority = 'Normal';
  if (!approved || status === 'Needs Research') priority = 'High';
  else if (match === 'Mismatch' || confidence < CONFIG.lowConfidenceThreshold) priority = 'High';
  else if (confidence < 0.85 || errorReason) priority = 'Medium';

  sheet.getRange(row, headerMap.category_match + 1).setValue(match);
  sheet.getRange(row, headerMap.priority + 1).setValue(priority);
  if (status === 'Reviewed' && !values[headerMap.reviewed_at]) {
    sheet.getRange(row, headerMap.reviewed_at + 1).setValue(new Date());
  }
  applyRowFormatting_(sheet, row, priority, match);
}

function refreshDashboard() {
  const spreadsheet = SpreadsheetApp.getActive();
  const source = spreadsheet.getSheetByName(CONFIG.evaluationSheet);
  const dashboard = getOrCreateSheet_(spreadsheet, CONFIG.dashboardSheet);
  dashboard.clear();

  dashboard.getRange('A1').setValue('AI Product Classification QA Dashboard');
  dashboard.getRange('A1:F1').merge();
  dashboard.getRange('A1').setFontSize(18).setFontWeight('bold').setBackground('#1f4e78').setFontColor('#ffffff');

  if (!source || source.getLastRow() < 2) {
    dashboard.getRange('A3').setValue('Import evaluation data, then refresh this dashboard.');
    return;
  }

  const headerMap = getHeaderMap_(source);
  const rows = source.getRange(2, 1, source.getLastRow() - 1, source.getLastColumn()).getValues();
  const total = rows.length;
  const reviewed = rows.filter(row => String(row[headerMap.review_status]) === 'Reviewed').length;
  const matches = rows.filter(row => String(row[headerMap.category_match]) === 'Match').length;
  const mismatches = rows.filter(row => String(row[headerMap.category_match]) === 'Mismatch').length;
  const highPriority = rows.filter(row => String(row[headerMap.priority]) === 'High').length;
  const lowConfidence = rows.filter(row => Number(row[headerMap.ai_confidence]) < CONFIG.lowConfidenceThreshold).length;
  const agreementRate = reviewed ? matches / reviewed : 0;
  const completion = total ? reviewed / total : 0;

  const metrics = [
    ['Metric', 'Value'],
    ['Total records', total],
    ['Reviewed records', reviewed],
    ['Review completion rate', completion],
    ['Reviewed category agreement rate', agreementRate],
    ['Category mismatches', mismatches],
    ['Low-confidence records', lowConfidence],
    ['High-priority records', highPriority]
  ];
  dashboard.getRange(3, 1, metrics.length, 2).setValues(metrics);
  dashboard.getRange('A3:B3').setFontWeight('bold').setBackground('#d9eaf7');
  dashboard.getRange('B6:B7').setNumberFormat('0.0%');

  const issueCounts = {};
  rows.forEach(row => {
    const reason = String(row[headerMap.error_reason] || 'No error');
    issueCounts[reason] = (issueCounts[reason] || 0) + 1;
  });
  const issueRows = [['Error reason', 'Records']].concat(
    Object.entries(issueCounts).sort((a, b) => b[1] - a[1])
  );
  dashboard.getRange(3, 4, issueRows.length, 2).setValues(issueRows);
  dashboard.getRange('D3:E3').setFontWeight('bold').setBackground('#d9eaf7');

  const queue = rows
    .filter(row => String(row[headerMap.priority]) === 'High')
    .map(row => [
      row[headerMap.record_id],
      row[headerMap.product_description],
      row[headerMap.ai_predicted_category],
      row[headerMap.ai_confidence],
      row[headerMap.reviewer_approved_category],
      row[headerMap.review_status]
    ]);
  const queueRows = [['Record ID', 'Product', 'AI category', 'Confidence', 'Approved category', 'Status']].concat(queue);
  dashboard.getRange(13, 1, queueRows.length, 6).setValues(queueRows);
  dashboard.getRange('A13:F13').setFontWeight('bold').setBackground('#f4cccc');
  dashboard.getRange(14, 4, Math.max(queue.length, 1), 1).setNumberFormat('0%');

  dashboard.setFrozenRows(1);
  dashboard.autoResizeColumns(1, 6);
}

function assignNextReviewItem() {
  const spreadsheet = SpreadsheetApp.getActive();
  const sheet = spreadsheet.getSheetByName(CONFIG.evaluationSheet);
  if (!sheet || sheet.getLastRow() < 2) return;

  const headerMap = getHeaderMap_(sheet);
  const rows = sheet.getRange(2, 1, sheet.getLastRow() - 1, sheet.getLastColumn()).getValues();
  const nextIndex = rows.findIndex(row =>
    String(row[headerMap.priority]) === 'High' &&
    String(row[headerMap.review_status]) !== 'Reviewed'
  );

  if (nextIndex === -1) {
    SpreadsheetApp.getUi().alert('No unreviewed high-priority records remain.');
    return;
  }
  spreadsheet.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange(nextIndex + 2, 1, 1, sheet.getLastColumn()));
}

function ensureEvaluationColumns_(sheet) {
  const existing = sheet.getRange(1, 1, 1, Math.max(sheet.getLastColumn(), 1)).getValues()[0];
  CONFIG.headers.forEach(header => {
    if (!existing.includes(header)) {
      sheet.getRange(1, sheet.getLastColumn() + 1).setValue(header);
      existing.push(header);
    }
  });
}

function formatEvaluationSheet_(sheet) {
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1, 1, sheet.getLastColumn())
    .setFontWeight('bold')
    .setBackground('#1f4e78')
    .setFontColor('#ffffff');
  sheet.autoResizeColumns(1, sheet.getLastColumn());
}

function formatGuideSheet_(sheet) {
  if (sheet.getLastRow() > 0) {
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, sheet.getLastColumn())
      .setFontWeight('bold')
      .setBackground('#1f4e78')
      .setFontColor('#ffffff');
    sheet.autoResizeColumns(1, sheet.getLastColumn());
  }
}

function applyRowFormatting_(sheet, row, priority, match) {
  const range = sheet.getRange(row, 1, 1, sheet.getLastColumn());
  range.setBackground(null);
  if (priority === 'High') range.setBackground('#fce8e6');
  else if (priority === 'Medium') range.setBackground('#fff2cc');
  else if (match === 'Match') range.setBackground('#e6f4ea');
}

function getHeaderMap_(sheet) {
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  return headers.reduce((map, header, index) => {
    map[String(header).trim()] = index;
    return map;
  }, {});
}

function getOrCreateSheet_(spreadsheet, name) {
  return spreadsheet.getSheetByName(name) || spreadsheet.insertSheet(name);
}

function getOrCreateSheetFromAliases_(spreadsheet, name, aliases) {
  const namedSheet = spreadsheet.getSheetByName(name);
  if (namedSheet) return namedSheet;

  for (const alias of aliases) {
    const importedSheet = spreadsheet.getSheetByName(alias);
    if (importedSheet) {
      importedSheet.setName(name);
      return importedSheet;
    }
  }
  return spreadsheet.insertSheet(name);
}
