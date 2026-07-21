"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { getMarginPreview, uploadCostPrices } from "../lib/api";
import { demoMarginRows, type MarginRow } from "../lib/margin-data";
import { Overview } from "./Overview";
import { ProductTable } from "./ProductTable";
import { Sidebar } from "./Sidebar";

type DataMode = "loading" | "live" | "demo" | "error";

export function Dashboard() {
  const [query, setQuery] = useState("");
  const [threshold, setThreshold] = useState(20);
  const [onlyAlerts, setOnlyAlerts] = useState(false);
  const [rows, setRows] = useState<MarginRow[]>(demoMarginRows);
  const [dataMode, setDataMode] = useState<DataMode>("loading");
  const [notice, setNotice] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const uploadInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let isCurrent = true;

    void getMarginPreview(threshold)
      .then((previewRows) => {
        if (!isCurrent) return;
        setRows(previewRows);
        setDataMode("live");
        setNotice("");
      })
      .catch((error: unknown) => {
        if (!isCurrent) return;
        setDataMode("demo");
        setNotice(error instanceof Error ? error.message : "Не удалось получить данные API.");
      });

    return () => {
      isCurrent = false;
    };
  }, [threshold]);

  const alertRows = useMemo(() => rows.filter((row) => row.percent < threshold), [rows, threshold]);
  const visibleRows = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();
    return rows.filter((row) => {
      const matchesQuery = `${row.sku} ${row.product}`.toLowerCase().includes(normalizedQuery);
      return matchesQuery && (!onlyAlerts || row.percent < threshold);
    });
  }, [onlyAlerts, query, rows, threshold]);

  const toggleAlerts = () => {
    if (!onlyAlerts) setQuery("");
    setOnlyAlerts((value) => !value);
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setDataMode("loading");
    setNotice("");
    try {
      const result = await uploadCostPrices(file);
      setRows(await getMarginPreview(threshold));
      setDataMode("live");
      setNotice(`Себестоимость обновлена: ${result.upserted} SKU.`);
    } catch (error) {
      setDataMode("error");
      setNotice(error instanceof Error ? error.message : "Не удалось загрузить CSV.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <main className="app-shell">
      <Sidebar alertCount={alertRows.length} />
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
          onlyAlerts={onlyAlerts}
          rows={rows}
          threshold={threshold}
          onToggleAlerts={toggleAlerts}
          onUploadClick={() => uploadInputRef.current?.click()}
        />
        <ProductTable
          onlyAlerts={onlyAlerts}
          query={query}
          rows={visibleRows}
          threshold={threshold}
          onQueryChange={setQuery}
          onThresholdChange={setThreshold}
        />
      </section>
    </main>
  );
}
