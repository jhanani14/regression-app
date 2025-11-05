import { useEffect, useState } from "react";
import api from "../api";

export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(url)
      .then((res) => setData(res.data))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading };
}
