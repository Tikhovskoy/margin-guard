import Image from "next/image";
import {
  calculatePortfolioMetrics,
  formatCurrency,
  type MarginRow,
} from "../lib/margin-data";

type DataMode = "loading" | "live" | "mock" | "demo" | "error";

type OverviewProps = {
  alertRows: MarginRow[];
  dataMode: DataMode;
  isUploading: boolean;
  notice: string;
  rows: MarginRow[];
  threshold: number;
  onSelectRow: (row: MarginRow) => void;
  onShowAlerts: () => void;
  onUploadClick: () => void;
};

const modeLabel: Record<DataMode, string> = {
  loading: "Подключаем API",
  live: "Реальные данные",
  mock: "Mock API",
  demo: "Локальный demo",
  error: "Ошибка загрузки",
};

const percent = (part: number, total: number) => total > 0 ? Math.max(0, part / total * 100) : 0;
const formatPercent = (value: number) => value.toLocaleString("ru-RU", { maximumFractionDigits: 1 });

export function Overview({
  alertRows,
  dataMode,
  isUploading,
  notice,
  rows,
  threshold,
  onSelectRow,
  onShowAlerts,
  onUploadClick,
}: OverviewProps) {
  const metrics = calculatePortfolioMetrics(rows);
  const sortedAlerts = [...alertRows].sort(
    (a, b) => (a.percent ?? Number.POSITIVE_INFINITY) - (b.percent ?? Number.POSITIVE_INFINITY),
  );
  const primaryRisk = sortedAlerts[0] ?? null;
  const riskShare = metrics.completeCount
    ? Math.round(alertRows.length / metrics.completeCount * 100)
    : 0;

  return (
    <>
      <header className="topbar">
        <Image className="mobile-brand" src="/brand/margin-guard-mark-v2.svg" alt="Margin Guard" width={28} height={28} />
        <div className="market-tabs" role="tablist" aria-label="Маркетплейс">
          <button type="button" role="tab" aria-selected="true">Wildberries</button>
          <button type="button" role="tab" aria-selected="false" disabled title="Нет данных Ozon">Ozon · нет данных</button>
        </div>
        <div className="top-meta">
          <span className={`data-state ${dataMode}`} role="status"><i />{modeLabel[dataMode]}</span>
        </div>
      </header>

      <section className="heading" id="overview">
        <div>
          <p className="eyebrow">Финансовый контроль · Wildberries</p>
          <h1>Контроль маржи</h1>
          <p className="heading-copy">Сначала — позиции, где предварительный результат ниже безопасного порога. Затем — состав учтённых расходов каждого SKU.</p>
        </div>
        <button className="primary" type="button" disabled={isUploading} onClick={onUploadClick}>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 14v5h14v-5" /></svg>
          {isUploading ? "Загружаем CSV…" : "Обновить себестоимость"}
        </button>
      </section>

      {notice && (
        <div className={`data-notice ${dataMode}`} role={dataMode === "error" ? "alert" : "status"}>
          <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8" /><path d="M10 6.5v4.5m0 3h.01" /></svg>
          <p>{notice}</p>
        </div>
      )}

      <section className="summary" aria-label="Сводка по марже">
        <article className="summary-cell">
          <div className="metric-label"><span>Предварительный результат</span><span>УЧТЁННЫЕ SKU</span></div>
          <strong className="metric-value">{formatCurrency(metrics.totalMargin)}</strong>
          <p className="metric-note">Выручка минус комиссии и известная себестоимость</p>
          <div className="composition" aria-label="Состав выручки">
            <span style={{ width: `${percent(metrics.totalCost, metrics.totalRevenue)}%` }} />
            <span style={{ width: `${percent(metrics.totalFees, metrics.totalRevenue)}%` }} />
            <span style={{ width: `${percent(metrics.totalMargin, metrics.totalRevenue)}%` }} />
          </div>
          <div className="composition-legend">
            <span>Себест. {formatPercent(percent(metrics.totalCost, metrics.totalRevenue))}%</span>
            <span>Комиссии {formatPercent(percent(metrics.totalFees, metrics.totalRevenue))}%</span>
            <span>Результат {formatPercent(percent(metrics.totalMargin, metrics.totalRevenue))}%</span>
          </div>
        </article>
        <article className="summary-cell">
          <div className="metric-label"><span>Взвешенная маржа</span><span>ПО {metrics.completeCount} SKU</span></div>
          <strong className="metric-value">{formatPercent(metrics.weightedMarginPercent)}%</strong>
          <p className="metric-note">Порог риска: <strong>{threshold}%</strong></p>
        </article>
        <article className="summary-cell">
          <div className="metric-label"><span>Ниже порога</span><span>ТРЕБУЕТ ДЕЙСТВИЯ</span></div>
          <strong className="metric-value risk-value">{alertRows.length} SKU</strong>
          <p className="metric-note">
            {riskShare}% рассчитанных SKU
            {metrics.incompleteCount > 0 ? ` · без себестоимости: ${metrics.incompleteCount}` : ""}
          </p>
        </article>
      </section>

      <section className="section" id="risks">
        <div className="section-head">
          <div><h2>Приоритет на сегодня</h2><p>Позиции отсортированы по отклонению от установленного порога.</p></div>
          <button className="text-action" type="button" onClick={onShowAlerts}>Показать в таблице</button>
        </div>
        <div className="priority">
          <div className="priority-main">
            {sortedAlerts.length ? sortedAlerts.slice(0, 3).map((row, index) => (
              <button className="priority-row" type="button" key={row.sku} onClick={() => onSelectRow(row)}>
                <span className="product">
                  <span className="product-index">{String(index + 1).padStart(2, "0")}</span>
                  <span><b>{row.product}</b><span>{row.sku}</span></span>
                </span>
                <span><small className="cell-label">Маржа</small><b className="cell-value risk-percent">{formatPercent(row.percent ?? 0)}%</b></span>
                <span><small className="cell-label">Результат</small><b className="cell-value">{formatCurrency(row.margin ?? 0)}</b></span>
                <span><small className="cell-label">До порога</small><b className="cell-value">{formatPercent(threshold - (row.percent ?? 0))} п.п.</b></span>
              </button>
            )) : (
              <div className="priority-empty"><span className="product-index safe">✓</span><div><b>Все позиции выше порога</b><span>Текущая выборка</span></div></div>
            )}
          </div>
          <aside className={`priority-aside ${primaryRisk ? "" : "safe"}`}>
            <span className="mono">{primaryRisk ? `−${formatPercent(threshold - (primaryRisk.percent ?? 0))} п.п. до порога` : "Рисков не обнаружено"}</span>
            <div>
              <h3>{primaryRisk ? `Проверьте «${primaryRisk.product}»` : "Маржа в безопасной зоне"}</h3>
              <p>{primaryRisk ? "Пересчитайте цену с учётом фактических удержаний и себестоимости." : "Продолжайте следить за изменением комиссий и себестоимости."}</p>
            </div>
            <button className="outline-button" type="button" disabled={!primaryRisk} onClick={() => primaryRisk && onSelectRow(primaryRisk)}>Разобрать экономику</button>
          </aside>
        </div>
      </section>
    </>
  );
}
