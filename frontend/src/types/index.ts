export type ExperimentMetrics = {
  mse?: number;
  rmse?: number;
  mae?: number;
  r2?: number;
  [k: string]: number | undefined;
};

export type ExperimentItem = {
  id: string;
  created_at?: string;
  target?: string;
  status?: string;
  metrics?: ExperimentMetrics;
};
