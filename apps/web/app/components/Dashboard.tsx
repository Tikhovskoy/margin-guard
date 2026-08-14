"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { getMarginPreview, uploadCostPrices } from "../lib/api";
import { demoMarginRows, type MarginRow } from "../lib/margin-data";
import { Overview } from "./Overview";
import { ProductTable } from "./ProductTable";
import { Sidebar } from "./Sidebar";
import { SkuDetailsDialog } from "./SkuDetailsDialog";

type DataMode = "loading" | "live" | "mock" | "demo" | "error";

export function Dashboard() {
  const [query, setQuery] = useState("");
  const [threshold, setThreshold] = useState(20);
  const [onlyAlerts, setOnlyAlerts] = useState(false);
  const [rows, setRows] = useState<MarginRow[]>(demoMarginRows);
  const [dataMode, setDataMode] = useState<DataMode>("loading");
  const [notice, setNotice] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [selectedRow, setSelectedRow] = useState<MarginRow | null>(null);
  const uploadInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let isCurrent = true;

    void getMarginPreview(threshold)
      .then((preview) => {
        if (!isCurrent) return;
        setRows(preview.rows);
        setDataMode(preview.sourceMode === "live" ? "live" : "mock");
        setNotice(
          preview.sourceMode === "mock"
            ? "Показаны тестовые операции mock API. Это демонстрационный расчёт."
            : "",
        );
      })
      .catch((error: unknown) => {
        if (!isCurrent) return;
        setDataMode("demo");
        const message = error instanceof Error ? error.message : "Не удалось получить данные API.";
        setNotice(`${message} Показан локальный демонстрационный набор.`);
      });

    return () => {
      isCurrent = false;
    };
  }, [threshold]);

  const alertRows = useMemo(
    () => rows.filter((row) => row.percent !== null && row.percent < threshold),
    [rows, threshold],
  );
  const visibleRows = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    return rows.filter((row) => {
      const matchesQuery = `${row.sku} ${row.product}`.toLowerCase().includes(normalizedQuery);
      return matchesQuery && (
        !onlyAlerts || (row.percent !== null && row.percent < threshold)
      );
    });
  }, [onlyAlerts, query, rows, threshold]);

  const showAlerts = () => {
    setQuery("");
    setOnlyAlerts(true);
    window.requestAnimationFrame(() => {
      document.getElementById("products")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setDataMode("loading");
    setNotice("");
    try {
      const result = await uploadCostPrices(file);
      const preview = await getMarginPreview(threshold);
      setRows(preview.rows);
      setDataMode(preview.sourceMode === "live" ? "live" : "mock");
      setNotice(
        `Загружено цен: ${result.upserted}. В текущем preview операций: ${preview.rows.length}.`,
      );
    } catch (error) {
      setDataMode("error");
      setNotice(error instanceof Error ? error.message : "Не удалось загрузить CSV.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <main className="app-shell">
      <Sidebar alertCount={alertRows.length} dataMode={dataMode} />
      <section className="workspace">
        <input
          ref={uploadInputRef}
          accept=".csv,text/csv"
          className="visually-hidden"
          type="file"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) void handleUpload(file);
            event.currentTarget.value = "";
          }}
        />
        <Overview
          alertRows={alertRows}
          dataMode={dataMode}
          isUploading={isUploading}
          notice={notice}
          rows={rows}
          threshold={threshold}
          onSelectRow={setSelectedRow}
          onShowAlerts={showAlerts}
          onUploadClick={() => uploadInputRef.current?.click()}
        />
        <ProductTable
          onlyAlerts={onlyAlerts}
          query={query}
          rows={visibleRows}
          threshold={threshold}
          onOnlyAlertsChange={setOnlyAlerts}
          onQueryChange={setQuery}
          onSelectRow={setSelectedRow}
          onThresholdChange={setThreshold}
        />
      </section>
      <nav className="mobile-bar" aria-label="Мобильная навигация">
        <a className="active" href="#overview">Обзор</a>
        <a href="#risks">Риски</a>
        <a href="#products">Товары</a>
      </nav>
      <SkuDetailsDialog row={selectedRow} onClose={() => setSelectedRow(null)} />
    </main>
  );
}
