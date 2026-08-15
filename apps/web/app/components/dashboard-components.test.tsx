import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";

import type { MarginRow } from "../lib/margin-data";
import { ProductTable } from "./ProductTable";
import { SkuDetailsDialog } from "./SkuDetailsDialog";

const incompleteRow: MarginRow = {
  sku: "WB-NO-COST",
  sourceOperationId: "mock-wb-no-cost",
  quantity: 2,
  product: "Товар без себестоимости",
  revenue: 1000,
  fees: 200,
  unitCost: null,
  cost: null,
  margin: null,
  percent: null,
  status: "incomplete",
  rrdId: null,
  srid: null,
  reportId: null,
};

describe("ProductTable", () => {
  it("does not render a zero margin when cost is missing", () => {
    const markup = renderToStaticMarkup(
      <ProductTable
        onlyAlerts={false}
        query=""
        rows={[incompleteRow]}
        threshold={20}
        onOnlyAlertsChange={vi.fn()}
        onQueryChange={vi.fn()}
        onSelectRow={vi.fn()}
        onThresholdChange={vi.fn()}
      />,
    );

    expect(markup).toContain("Нет себестоимости");
    expect(markup).not.toContain("0%");
  });
});

describe("SkuDetailsDialog", () => {
  it("explains why an incomplete calculation is blocked", () => {
    const markup = renderToStaticMarkup(
      <SkuDetailsDialog row={incompleteRow} onClose={vi.fn()} />,
    );

    expect(markup).toContain("Расчёт заблокирован");
    expect(markup).toContain("Нет данных");
    expect(markup).toContain("Не рассчитана");
  });
});
