import {
  mapMarginPreviewItems,
  type MarginPreviewItem,
  type MarginRow,
} from "./margin-data";

type MarginPreview = {
  marketplace: string;
  data_mode: "mock" | "live";
  items: MarginPreviewItem[];
};

export type MarginPreviewResult = {
  rows: MarginRow[];
  sourceMode: "mock" | "live";
};

type UploadResponse = { upserted: number };

async function readError(response: Response) {
  const body = await response.json().catch(() => null) as { detail?: string } | null;
  return body?.detail ?? "Сервис временно недоступен.";
}

export async function getMarginPreview(threshold: number): Promise<MarginPreviewResult> {
  const response = await fetch(`/api/margins?threshold_percent=${threshold}`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error(await readError(response));

  const preview = await response.json() as MarginPreview;
  return {
    rows: mapMarginPreviewItems(preview.items),
    sourceMode: preview.data_mode,
  };
}

export async function uploadCostPrices(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/api/cost-prices", { method: "POST", body: formData });
  if (!response.ok) throw new Error(await readError(response));
  return response.json() as Promise<UploadResponse>;
}
