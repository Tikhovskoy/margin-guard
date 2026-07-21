"use client";

import { useMemo, useState } from "react";
import { marginRows } from "../lib/margin-data";
import { Overview } from "./Overview";
import { ProductTable } from "./ProductTable";
import { Sidebar } from "./Sidebar";

export function Dashboard() {
  const [query, setQuery] = useState("");
  const [threshold, setThreshold] = useState(20);
  const [onlyAlerts, setOnlyAlerts] = useState(false);

  const alertRows = useMemo(
    () => marginRows.filter((row) => row.percent < threshold),
    [threshold],
  );

  const visibleRows = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    return marginRows.filter((row) => {
      const matchesQuery = `${row.sku} ${row.product}`
        .toLowerCase()
        .includes(normalizedQuery);
      return matchesQuery && (!onlyAlerts || row.percent < threshold);
    });
  }, [onlyAlerts, query, threshold]);

  const toggleAlerts = () => {
    if (!onlyAlerts) {
      setQuery("");
    }
    setOnlyAlerts((value) => !value);
  };

  return (
    <main className="app-shell">
      <Sidebar alertCount={alertRows.length} />
      <section className="workspace">
        <Overview
          alertRows={alertRows}
          onlyAlerts={onlyAlerts}
          onToggleAlerts={toggleAlerts}
          threshold={threshold}
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
