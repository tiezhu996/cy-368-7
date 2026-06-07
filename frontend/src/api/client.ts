import { API_BASE_URL } from "../constants/app";
import type { OverviewResponse, BattleListResponse, BattleChallenge, BattleActionRequest } from "../types";

export async function fetchOverview(): Promise<OverviewResponse> {
  const response = await fetch(`${API_BASE_URL}/overview`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Overview request failed: ${response.status}`);
  }

  return response.json() as Promise<OverviewResponse>;
}

export async function fetchBattles(): Promise<BattleListResponse> {
  const response = await fetch(`${API_BASE_URL}/battles`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Battles request failed: ${response.status}`);
  }

  return response.json() as Promise<BattleListResponse>;
}

export async function confirmBattle(challengeId: number): Promise<BattleChallenge> {
  const response = await fetch(`${API_BASE_URL}/battles/confirm`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ challenge_id: challengeId } as BattleActionRequest),
  });

  if (!response.ok) {
    throw new Error(`Confirm battle failed: ${response.status}`);
  }

  return response.json() as Promise<BattleChallenge>;
}

export async function cancelBattle(challengeId: number): Promise<BattleChallenge> {
  const response = await fetch(`${API_BASE_URL}/battles/cancel`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ challenge_id: challengeId } as BattleActionRequest),
  });

  if (!response.ok) {
    throw new Error(`Cancel battle failed: ${response.status}`);
  }

  return response.json() as Promise<BattleChallenge>;
}
