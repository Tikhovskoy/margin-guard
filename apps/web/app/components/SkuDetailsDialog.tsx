"use client";

import { useEffect, useRef } from "react";
import { formatCurrency, type MarginRow } from "../lib/margin-data";

type SkuDetailsDialogProps = {
  row: MarginRow | null;
  onClose: () => void;
};

export function SkuDetailsDialog({ row, onClose }: SkuDetailsDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (row && !dialog.open) dialog.showModal();
    if (!row && dialog.open) dialog.close();
  }, [row]);

  const formatNullableCurrency = (value: number | null) => (
    value === null ? "Нет данных" : formatCurrency(value)
  );

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby="sku-dialog-title"
      onCancel={onClose}
      onClick={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
      onClose={onClose}
    >
      {row && (
        <>
          <div className="dialog-head">
            <div>
              <h3 id="sku-dialog-title">{row.product}</h3>
              <p>{row.sku}</p>
            </div>
            <button className="dialog-close" type="button" aria-label="Закрыть" onClick={onClose}>
              <svg viewBox="0 0 16 16" aria-hidden="true">
                <path d="M3.5 3.5l9 9m0-9-9 9" />
              </svg>
            </button>
          </div>
          {row.margin === null || row.cost === null ? (
            <p className="equation" role="status">
              Расчёт заблокирован: загрузите себестоимость для этого SKU.
            </p>
          ) : (
            <p className="equation" aria-label="Формула предварительного результата">
              {formatCurrency(row.revenue)} − {formatCurrency(row.fees)} − {formatCurrency(row.cost)} = {formatCurrency(row.margin)}
            </p>
          )}
          <div className="detail-grid">
            <div><span>Выручка</span><b>{formatCurrency(row.revenue)}</b></div>
            <div><span>Комиссии</span><b>{formatCurrency(row.fees)}</b></div>
            <div><span>Себестоимость</span><b>{formatNullableCurrency(row.cost)}</b></div>
            <div><span>Маржа</span><b>{row.percent === null ? "Не рассчитана" : `${row.percent.toLocaleString("ru-RU", { maximumFractionDigits: 1 })}%`}</b></div>
          </div>
        </>
      )}
    </dialog>
  );
}
