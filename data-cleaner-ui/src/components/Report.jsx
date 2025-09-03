import React, { useState } from 'react';

const displayValue = (value, fallback = 'N/A') => value ?? fallback;

function Report({ data }) {
    const [showColumns, setShowColumns] = useState(false);
    const [showPreviewAll, setShowPreviewAll] = useState(false);

    if (!data || !data.report) return <div>Error: Report data is missing or invalid.</div>;

    const { report, recommendations = [], preview = [], columns = [] } = data;
    const overview = report.overview || {};
    const cols = report.column_details || {};

    return (
        <div className="results-container">
            <div className="recommendations-box">
                <h3>Recommended Actions</h3>
                <ul>
                    {recommendations.length ? (
                        recommendations.map((rec, i) => <li key={i}>{rec}</li>)
                    ) : (
                        <li>No recommendations — data looks good.</li>
                    )}
                </ul>
            </div>

            <h3>Data Quality Overview</h3>
            <div className="overview-grid">
                <div className="stat-card">
                    <div className="icon">#</div>
                    <div>
                        <div className="value">{displayValue(overview.rows, 0)}</div>
                        <div className="label">Rows</div>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="icon">C</div>
                    <div>
                        <div className="value">{displayValue(overview.columns, 0)}</div>
                        <div className="label">Columns</div>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="icon">!</div>
                    <div>
                        <div className="value">{displayValue(overview.total_missing_values, 0)}</div>
                        <div className="label">Missing Values</div>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="icon">D</div>
                    <div>
                        <div className="value">{displayValue(overview.duplicate_rows, 0)}</div>
                        <div className="label">Duplicate Rows</div>
                    </div>
                </div>
            </div>

            <div className="accordion">
                <div className="accordion-header" style={{ cursor: 'pointer' }} onClick={() => setShowColumns(s => !s)}>
                    <h3 style={{ margin: 0 }}>Detailed Column Analysis</h3>
                    <button className="analyzeBtn" style={{ padding: '6px 10px' }} onClick={(e) => { e.stopPropagation(); setShowColumns(s => !s); }}>{showColumns ? 'Hide' : 'Show'}</button>
                </div>
                <div className={`accordion-body ${showColumns ? 'open' : ''}`}>
                    <div className="columns-grid">
                        {(() => {
                            const allCols = Object.entries(cols);
                            const errorCols = allCols.filter(([, details]) => details.has_problem);

                            // When collapsed: show up to 3 error columns (or first 3 if no errors). When expanded: show all columns.
                            const listToRender = showColumns ? allCols : (errorCols.length ? errorCols.slice(0, 3) : allCols.slice(0, 3));

                            return listToRender.map(([colName, details]) => {
                                // Highlight when backend marked has_problem (missing values or duplicate columns)
                                const problem = !!details.has_problem;
                                return (
                                    <div key={colName} className={`column-card ${problem ? 'problem' : ''}`}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>
                                                {colName}{details.has_problem ? <span className="issue-badge" style={{ marginLeft: 12 }}>Issue</span> : null}
                                            </div>
                                            <div className="dtype-badge">{displayValue(details.dtype, '')}</div>
                                        </div>
                                        <ul className="column-stats">
                                            <li><span>Missing</span><strong>{displayValue(details.missing_values, 0)}</strong></li>
                                            <li><span>Unique</span><strong>{displayValue(details.unique_values, 0)}</strong></li>
                                            <li><span>Outliers</span><strong>{displayValue(details.outlier_count, 0)}</strong></li>
                                        </ul>
                                        <div style={{ marginTop: 8 }}>
                                            <div className="progress-bar-container">
                                                <div className="progress-bar" style={{ width: `${displayValue(details.missing_percentage, 0)}%` }} />
                                            </div>
                                        </div>
                                        {details.reasons && details.reasons.length > 0 && (
                                            <div style={{ marginTop: 10, color: 'var(--text-secondary)', fontSize: 13 }}>
                                                <strong>Notes:</strong> {details.reasons.join(' • ')}
                                            </div>
                                        )}
                                    </div>
                                );
                            });
                        })()}
                    </div>
                </div>
            </div>

            <div className="accordion" style={{ marginTop: '1.5rem' }}>
                <div className="accordion-header" style={{ cursor: 'pointer' }} onClick={() => setShowPreviewAll(s => !s)}>
                    <h3 style={{ margin: 0 }}>Data Preview</h3>
                </div>
                <div className={`accordion-body ${showPreviewAll ? 'open' : ''}`}>
                    <div className="preview-table-wrapper compact-preview">
                        <table>
                            <thead>
                                <tr>{columns.map((c) => <th key={c}>{c}</th>)}</tr>
                            </thead>
                            <tbody>
                                {(showPreviewAll ? preview : preview.slice(0, 5)).map((row, i) => (
                                    <tr key={i}>
                                        {columns.map((c) => <td key={c}>{String(row[c] ?? '')}</td>)}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {preview.length > 5 && (
                            <div style={{ textAlign: 'center', marginTop: 8 }}>
                                <button className="cleanBtn" onClick={() => setShowPreviewAll(s => !s)}>{showPreviewAll ? 'Show less' : `Show all (${preview.length})`}</button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Report;