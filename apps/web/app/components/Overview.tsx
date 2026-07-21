import { formatCurrency, marginRows, type MarginRow } from "../lib/margin-data";

type OverviewProps = {
  alertRows: MarginRow[];
  onlyAlerts: boolean;
  onToggleAlerts: () => void;
  threshold: number;
};

const chartValues = [34, 41, 38, 55, 49, 66, 61, 74, 69, 82, 78, 92];

export function Overview({ alertRows, onlyAlerts, onToggleAlerts, threshold }: OverviewProps) {
  const totalRevenue = marginRowsTotal("revenue");
  const totalMargin = marginRowsTotal("margin");

  return (
    <>
      <header className="topbar">
        <div className="market-select"><span className="market-mark">W</span><div><small>Маркетплейс</small><b>Wildberries</b></div><span className="chevron">⌄</span></div>
        <div className="top-actions">
          <button className="period-button">Последние 7 дней <span>⌄</span></button>
          <button className="round-button" aria-label="Уведомления"><span className="notification-dot" />◇</button>
          <button className="profile-button" aria-label="Профиль Виктора Тиховского">ВТ</button>
        </div>
      </header>

      <section className="intro" id="overview">
        <div>
          <p className="eyebrow"><span /> Финансовый радар</p>
          <h1>Маржа под контролем.<br /><em>Рост — в фокусе.</em></h1>
          <p className="intro-copy">Вся экономика продаж в одном ритме: прибыль, риски и точки роста без информационного шума.</p>
        </div>
        <button className="upload-button"><span>＋</span> Загрузить себестоимость</button>
      </section>

      <section className="overview-grid">
        <article className="pulse-card">
          <div className="pulse-topline"><span>Чистая маржинальная прибыль</span><span className="live-pill"><i /> LIVE</span></div>
          <strong>{formatCurrency(totalMargin)}</strong>
          <div className="delta"><b>↗ 12,8%</b><span>к прошлой неделе</span></div>
          <div className="chart" aria-label="График роста маржинальной прибыли">
            <div className="chart-glow" />
            {chartValues.map((value, index) => <i key={index} style={{ height: `${value}%` }} />)}
            <span className="chart-marker"><b>₽ 2 026</b><i /></span>
          </div>
          <div className="chart-axis"><span>15 июл</span><span>17 июл</span><span>19 июл</span><span>Сегодня</span></div>
        </article>

        <div className="metric-stack">
          <article className="premium-metric">
            <div className="metric-heading"><span className="metric-icon revenue">↗</span><small>Выручка</small><b>+8,4%</b></div>
            <strong>{formatCurrency(totalRevenue)}</strong>
            <p>за последние 7 дней</p>
            <div className="micro-bars">{[45, 58, 52, 70, 62, 76, 89].map((value) => <i key={value} style={{ height: `${value}%` }} />)}</div>
          </article>
          <article className="premium-metric">
            <div className="metric-heading"><span className="metric-icon margin">%</span><small>Средняя маржа</small><b>+3,4 п.п.</b></div>
            <strong>29,2%</strong>
            <p>цель на период: 32%</p>
            <div className="progress"><i style={{ width: "76%" }} /><span /></div>
          </article>
        </div>

        <article className="risk-card" id="alerts">
          <div className="risk-orbit"><span>{alertRows.length}</span><i /><i /></div>
          <p>SKU требуют внимания</p>
          <small>Маржа ниже порога {threshold}%</small>
          <div className="risk-list">
            {alertRows.slice(0, 2).map((row) => <div key={row.sku}><span>{row.sku}</span><b>{row.percent}%</b></div>)}
          </div>
          <button onClick={onToggleAlerts}>{onlyAlerts ? "Показать весь портфель" : "Разобрать риски"}<span>→</span></button>
        </article>
      </section>
    </>
  );
}

function marginRowsTotal(field: "revenue" | "margin") {
  return marginRows.reduce((total, row) => total + row[field], 0);
}
