import { formatCurrency, type MarginRow } from "../lib/margin-data";

type ProductTableProps = {
  onlyAlerts: boolean;
  query: string;
  rows: MarginRow[];
  threshold: number;
  onQueryChange: (value: string) => void;
  onThresholdChange: (value: number) => void;
};

const statusLabel = {
  healthy: "Стабильно",
  attention: "Наблюдать",
  critical: "Низкая маржа",
};

export function ProductTable({ onlyAlerts, query, rows, threshold, onQueryChange, onThresholdChange }: ProductTableProps) {
  return (
    <section className="products-panel" id="margins">
      <div className="panel-heading">
        <div><p className="section-kicker">ПОРТФЕЛЬ</p><h2>{onlyAlerts ? "Товары в зоне риска" : "Юнит-экономика по SKU"}</h2></div>
        <div className="panel-summary"><span><i className="healthy-dot" />{rows.length} позиций</span><button aria-label="Дополнительные действия">•••</button></div>
      </div>

      <div className="toolbar">
        <label className="search-field"><span>⌕</span><input value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Найти товар или SKU" /></label>
        <label className="threshold-field">Alert ниже<input type="number" min="1" max="99" value={threshold} onChange={(event) => onThresholdChange(Number(event.target.value))} /><span>%</span></label>
        <button className="filter-button">Фильтры <span>＋</span></button>
      </div>

      <div className="table-wrap">
        <table>
          <thead><tr><th>Товар</th><th>Выручка</th><th>Комиссии</th><th>Себестоимость</th><th>Маржа</th><th>Состояние</th></tr></thead>
          <tbody>
            {rows.map((row, index) => {
              const status = row.percent < threshold ? "critical" : row.status;
              return <tr key={row.sku} style={{ animationDelay: `${index * 55}ms` }}>
                <td><div className={`product-thumb tone-${(index % 4) + 1}`}><span>{row.product.slice(0, 1)}</span></div><div className="product-name"><b>{row.product}</b><span>{row.sku}</span></div></td>
                <td><b>{formatCurrency(row.revenue)}</b></td>
                <td>{formatCurrency(row.fees)}</td>
                <td>{formatCurrency(row.cost)}</td>
                <td><b>{formatCurrency(row.margin)}</b><span className="margin-percent">{row.percent}%</span></td>
                <td><em className={`status ${status}`}><i />{statusLabel[status]}</em></td>
              </tr>;
            })}
          </tbody>
        </table>
        {!rows.length && <div className="empty-state"><span>⌕</span><b>Ничего не найдено</b><p>Измените запрос или значение порога</p></div>}
      </div>
      <footer className="table-footer"><span>Обновлено несколько секунд назад</span><button>Смотреть полный отчёт <i>→</i></button></footer>
    </section>
  );
}
