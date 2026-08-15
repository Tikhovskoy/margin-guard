"use client";

import { useMemo, useState } from "react";
import { formatCurrency, type MarginRow, type MarginStatus } from "../lib/margin-data";

type SortKey = "quantity" | "revenue" | "fees" | "cost" | "margin" | "percent";
type SortDirection = "asc" | "desc";

type ProductTableProps = {
  onlyAlerts: boolean;
  query: string;
  rows: MarginRow[];
  threshold: number;
  onOnlyAlertsChange: (value: boolean) => void;
  onQueryChange: (value: string) => void;
  onSelectRow: (row: MarginRow) => void;
  onThresholdChange: (value: number) => void;
};

const statusLabel: Record<MarginStatus, string> = {
  healthy: "Стабильно",
  attention: "Наблюдать",
  critical: "Ниже порога",
  incomplete: "Нет себестоимости",
};

const columns: Array<{ key: SortKey; label: string }> = [
  { key: "quantity", label: "Количество" },
  { key: "revenue", label: "Выручка" },
  { key: "fees", label: "Комиссии" },
  { key: "cost", label: "Себестоимость" },
  { key: "margin", label: "Маржа" },
  { key: "percent", label: "Маржа, %" },
];

const formatPercent = (value: number) => value.toLocaleString("ru-RU", { maximumFractionDigits: 1 });
const formatNullableCurrency = (value: number | null) => value === null ? "—" : formatCurrency(value);

function getStatus(percent: number | null, threshold: number): MarginStatus {
  if (percent === null) return "incomplete";
  if (percent < threshold) return "critical";
  if (percent < threshold + 5) return "attention";
  return "healthy";
}

export function ProductTable({
  onlyAlerts,
  query,
  rows,
  threshold,
  onOnlyAlertsChange,
  onQueryChange,
  onSelectRow,
  onThresholdChange,
}: ProductTableProps) {
  const [sortKey, setSortKey] = useState<SortKey>("percent");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const sortedRows = useMemo(() => [...rows].sort((a, b) => {
    const aValue = a[sortKey] ?? Number.POSITIVE_INFINITY;
    const bValue = b[sortKey] ?? Number.POSITIVE_INFINITY;
    const result = aValue - bValue;
    return sortDirection === "asc" ? result : -result;
  }), [rows, sortDirection, sortKey]);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDirection((current) => current === "asc" ? "desc" : "asc");
      return;
    }
    setSortKey(key);
    setSortDirection("asc");
  };

  const sortLabel = (key: SortKey, label: string) => {
    if (key !== sortKey) return `${label}: сортировать по возрастанию`;
    return `${label}: сортировать по ${sortDirection === "asc" ? "убыванию" : "возрастанию"}`;
  };

  return (
    <section className="section" id="products">
      <div className="section-head"><div><h2>Экономика по SKU</h2><p>Предварительный результат: выручка − комиссии − известная себестоимость.</p></div></div>
      <div className="panel">
        <div className="toolbar">
          <label className="search">
            <span className="visually-hidden">Найти товар или SKU</span>
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8" /><path d="m16 16 4 4" /></svg>
            <input type="search" value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Найти товар или SKU" />
          </label>
          <label className="threshold">Порог ниже
            <input
              type="number"
              min="1"
              max="99"
              value={threshold}
              aria-label="Порог маржи"
              onChange={(event) => {
                const value = Number(event.target.value);
                if (Number.isFinite(value)) onThresholdChange(Math.max(1, Math.min(99, value)));
              }}
            />
            <span>%</span>
          </label>
          <label className="check"><input type="checkbox" checked={onlyAlerts} onChange={(event) => onOnlyAlertsChange(event.target.checked)} />Только риски</label>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Товар</th>
                {columns.map((column) => (
                  <th key={column.key} aria-sort={sortKey === column.key ? (sortDirection === "asc" ? "ascending" : "descending") : "none"}>
                    <button type="button" aria-label={sortLabel(column.key, column.label)} onClick={() => handleSort(column.key)}>
                      {column.label}<span aria-hidden="true">{sortKey === column.key ? (sortDirection === "asc" ? " ↑" : " ↓") : " ↕"}</span>
                    </button>
                  </th>
                ))}
                <th>Состояние</th>
              </tr>
            </thead>
            <tbody>
              {sortedRows.map((row) => {
                const status = getStatus(row.percent, threshold);
                return (
                  <tr
                    key={row.sourceOperationId}
                    tabIndex={0}
                    onClick={() => onSelectRow(row)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        onSelectRow(row);
                      }
                    }}
                  >
                    <td><div className="table-product"><b>{row.product}</b><span>{row.sku}</span></div></td>
                    <td className="number" data-label="Количество">{row.quantity}</td>
                    <td className="number" data-label="Выручка">{formatCurrency(row.revenue)}</td>
                    <td className="number" data-label="Комиссии">{formatCurrency(row.fees)}</td>
                    <td className="number" data-label="Себестоимость">{formatNullableCurrency(row.cost)}</td>
                    <td className="number" data-label="Результат">{formatNullableCurrency(row.margin)}</td>
                    <td className="number" data-label="Маржа, %">{row.percent === null ? "—" : `${formatPercent(row.percent)}%`}</td>
                    <td><span className={`status ${status}`}>{statusLabel[status]}</span></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {!sortedRows.length && <div className="empty"><b>Совпадений нет</b><br />Измените запрос или порог маржи.</div>}
        </div>
        <footer className="panel-footer">
          <span>{sortedRows.length} {sortedRows.length === 1 ? "позиция" : sortedRows.length > 1 && sortedRows.length < 5 ? "позиции" : "позиций"}</span>
          <span>Источник: {onlyAlerts ? "SKU ниже заданного порога" : "текущий preview"}</span>
        </footer>
      </div>
    </section>
  );
}
