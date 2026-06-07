export interface FeatureItem {
  id: number;
  title: string;
  description: string;
  status: string;
  metric: string;
}

export interface KpiItem {
  label: string;
  value: string;
  trend: string;
  tone: string;
}

export interface OperationRecord {
  key: string;
  name: string;
  owner: string;
  status: string;
  metric: string;
  priority: string;
}

export interface OverviewResponse {
  appName: string;
  appCode: string;
  description: string;
  features: FeatureItem[];
  kpis: KpiItem[];
  records: OperationRecord[];
}

export interface TeamInfo {
  id: number;
  name: string;
  leader_name: string;
  member_count: number;
}

export interface BattleChallenge {
  id: number;
  challenger_team: TeamInfo;
  challenged_team: TeamInfo;
  venue_name: string;
  battle_time: string;
  status: "pending" | "confirmed" | "cancelled";
  message: string | null;
  created_at: string;
  updated_at: string;
}

export interface BattleListResponse {
  pending: BattleChallenge[];
  confirmed: BattleChallenge[];
  pending_count: number;
}

export interface BattleActionRequest {
  challenge_id: number;
}
