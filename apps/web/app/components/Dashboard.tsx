"use client";

import { useMemo, useState } from "react";
import { formatCurrency, marginRows } from "../lib/margin-data";

const statusLabel = { healthy: "В норме", attention: "Проверить", critical: "Низкая маржа" };

export function Dashboard() {
  const [query, setQuery] = useState("");
  const [threshold, setThreshold] = useState(20);
  const [onlyAlerts, setOnlyAlerts] = useState(false);
  const visibleRows = useMemo(() => marginRows.filter((row) => {
    const matchesQuery = `${row.sku} ${row.product}`.toLowerCase().includes(query.toLowerCase());
    return matchesQuery && (!onlyAlerts || row.percent < threshold);
  }), [onlyAlerts, query, threshold]);
  const totalRevenue = marginRows.reduce((total, row) => total + row.revenue, 0);
  const totalMargin = marginRows.reduce((total, row) => total + row.margin, 0);
  const alertRows = marginRows.filter((row) => row.percent < threshold);

  return <main className="shell">
    <aside className="sidebar"><div className="brand"><span className="brand-mark">M</span><span>margin-guard</span></div><nav aria-label="Навигация"><a className="nav-link active" href="#overview">▦ Обзор</a><a className="nav-link" href="#margins">◫ Маржа по SKU</a><a className="nav-link" href="#alerts">◉ Уведомления <b>{alertRows.length}</b></a><a className="nav-link" href="#cost">↑ Себестоимость</a></nav><div className="sidebar-footer"><span className="live-dot" />Данные обновлены сейчас</div></aside>
    <section className="workspace"><header className="topbar"><div><p className="eyebrow">WILDBERRIES · MOCK MODE</p><h1>Контроль маржи</h1></div><div className="header-actions"><button className="icon-button" aria-label="Уведомления">◌</button><button className="avatar" aria-label="Профиль">ВТ</button></div></header>
      <section id="overview" className="hero-grid"><article className="balance-card"><p>Маржинальная прибыль</p><strong>{formatCurrency(totalMargin)}</strong><span>↗ 12,8% <i>к прошлой неделе</i></span><div className="sparkline">{Array.from({ length: 8 }).map((_, index) => <i key={index} />)}</div></article><article className="metric-card"><span>Выручка</span><strong>{formatCurrency(totalRevenue)}</strong><small>За последние 7 дней</small></article><article className="metric-card"><span>Средняя маржа</span><strong>29,2%</strong><small className="positive">↑ 3,4 п.п.</small></article><article className="metric-card warning"><span>Требуют внимания</span><strong>{alertRows.length} SKU</strong><small>Ниже порога {threshold}%</small></article></section>
      <section id="alerts" className="alert-banner"><div className="alert-icon">!</div><div><b>Есть товары с низкой маржой</b><p>{alertRows.map((row) => `${row.sku} · ${row.percent}%`).join("  ·  ")} — проверьте цену или себестоимость.</p></div><button onClick={() => setOnlyAlerts((value) => !value)}>{onlyAlerts ? "Показать всё" : "Показать SKU"} →</button></section>
      <section id="margins" className="panel"><div className="panel-heading"><div><h2>Маржа по SKU</h2><p>Актуальный расчёт с учётом комиссий и себестоимости</p></div><button className="primary-button">↑ Загрузить CSV</button></div><div className="toolbar"><label className="search">⌕<input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Поиск по SKU или товару" /></label><label className="threshold">Порог alert <input type="number" min="1" max="99" value={threshold} onChange={(event) => setThreshold(Number(event.target.value))} />%</label></div><div className="table-wrap"><table><thead><tr><th>Товар</th><th>Выручка</th><th>Комиссии</th><th>Себестоимость</th><th>Маржа</th><th>Статус</th></tr></thead><tbody>{visibleRows.map((row) => <tr key={row.sku}><td><b>{row.product}</b><span>{row.sku}</span></td><td>{formatCurrency(row.revenue)}</td><td>{formatCurrency(row.fees)}</td><td>{formatCurrency(row.cost)}</td><td><b>{formatCurrency(row.margin)}</b><span className="percent">{row.percent}%</span></td><td><em className={`status ${row.percent < threshold ? "critical" : row.status}`}>{row.percent < threshold ? "Низкая маржа" : statusLabel[row.status]}</em></td></tr>)}</tbody></table></div></section>
    </section>
  </main>;
}
