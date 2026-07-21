import { formatCurrency, type MarginRow } from "../lib/margin-data";

type OverviewProps = {
  alertRows: MarginRow[];
  dataMode: "loading" | "live" | "demo" | "error";
  isUploading: boolean;
  notice: string;
  onlyAlerts: boolean;
  rows: MarginRow[];
  threshold: number;
  onToggleAlerts: () => void;
  onUploadClick: () => void;
};

const chartValues = [34, 41, 38, 55, 49, 66, 61, 74, 69, 82, 78, 92];

const modeLabel = {
  loading: "Подключаем API",
  live: "Данные из API",
  demo: "Демо-данные",
  error: "Ошибка загрузки",
};

export function Overview({
  alertRows,
  dataMode,
  isUploading,
  notice,
  onlyAlerts,
  rows,
  threshold,
  onToggleAlerts,
  onUploadClick,
}: OverviewProps) {
  const totalRevenue = rows.reduce((total, row) => total + row.revenue, 0);
  const totalMargin = rows.reduce((total, row) => total + row.margin, 0);
  const averageMargin = rows.length
    ? rows.reduce((total, row) => total + row.percent, 0) / rows.length
    : 0;

  return (
    <>
      <header className="topbar">
        <div className="market-select"><span className="market-mark">W</span><div><small>Маркетплейс</small><b>Wildberries</b></div><span className="chevron">⌄</span></div>
        <div className="top-actions">
          <span className={`source-state ${dataMode}`}><i />{modeLabel[dataMode]}</span>
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
        <button className="upload-button" disabled={isUploading} onClick={onUploadClick}><span>＋</span>{isUploading ? "Загружаем CSV…" : "Загрузить себестоимость"}</button>
      </section>

      {notice && <div className={`data-notice ${dataMode}`} role="status"><span>{dataMode === "live" ? "✓" : "i"}</span><p>{notice}</p></div>}

      <section className="overview-grid">
        <article className="pulse-card">
          <div className="pulse-topline"><span>Чистая маржинальная прибыль</span><span className="live-pill"><i /> {dataMode === "live" ? "LIVE" : "DEMO"}</span></div>
          <strong>{formatCurrency(totalMargin)}</strong>
          <div className="delta"><b>↗ 12,8%</b><span>к прошлой неделе</span></div>
          <div className="chart" aria-label="График роста маржинальной прибыли">
            <div className="chart-glow" />
            {chartValues.map((value, index) => <i key={index} style={{ height: `${value}%` }} />)}
            <span className="chart-marker"><b>{formatCurrency(totalMargin)}</b><i /></span>
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
            <strong>{averageMargin.toLocaleString("ru-RU", { maximumFractionDigits: 1 })}%</strong>
            <p>цель на период: 32%</p>
            <div className="progress"><i style={{ width: `${Math.min(100, averageMargin / 32 * 100)}%` }} /><span /></div>
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
