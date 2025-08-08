#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yapılandırılmış AI çıktı şemaları (Pydantic v2)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class PercentageItem(BaseModel):
    name: str = Field(..., description="Kategori/isim")
    count: int = Field(0, ge=0, description="Adet")
    percent: int = Field(0, ge=0, le=100, description="Yüzde (0-100)")


class ManagerSummary(BaseModel):
    critical_findings: List[str] = Field(default_factory=list)
    urgent_actions: List[str] = Field(default_factory=list)
    grade: Optional[str] = Field(None, description="A-F ölçeği")
    management_recommendations: List[str] = Field(default_factory=list)


class KPI(BaseModel):
    equipment_distribution: List[PercentageItem] = Field(default_factory=list)
    shift_distribution: List[PercentageItem] = Field(default_factory=list)
    issue_distribution: List[PercentageItem] = Field(default_factory=list)
    mtbf_minutes: Optional[float] = None
    mttr_minutes: Optional[float] = None
    pareto_top10: List[PercentageItem] = Field(default_factory=list)

    @model_validator(mode="after")
    def _normalize_percents(self) -> "KPI":
        # Her bir yüzde listesinde toplamın 100 olmasını garanti etmeye çalış
        def fix(items: List[PercentageItem]) -> List[PercentageItem]:
            if not items:
                return items
            s = sum(i.percent for i in items)
            diff = 100 - s
            if diff != 0:
                items[-1].percent = max(0, min(100, items[-1].percent + diff))
            return items

        self.equipment_distribution = fix(self.equipment_distribution)
        self.shift_distribution = fix(self.shift_distribution)
        self.issue_distribution = fix(self.issue_distribution)
        self.pareto_top10 = fix(self.pareto_top10)
        return self


class ActionItem(BaseModel):
    title: str
    priority: Optional[int] = Field(None, ge=1, le=10)
    difficulty: Optional[str] = Field(None, description="Kolay/Orta/Zor")
    duration_days: Optional[int] = Field(None, ge=0)
    owner: Optional[str] = None
    metric: Optional[str] = None


class Trend(BaseModel):
    last7: Optional[int] = None
    prev7: Optional[int] = None
    delta: Optional[int] = None
    direction: Optional[str] = Field(None, description="↑/↓/=")


class AnalysisReport(BaseModel):
    manager_summary: ManagerSummary = Field(default_factory=ManagerSummary)
    kpi: KPI = Field(default_factory=KPI)
    root_causes: List[PercentageItem] = Field(default_factory=list)
    hidden_findings: List[str] = Field(default_factory=list)
    action_plan: List[ActionItem] = Field(default_factory=list)
    trend: Trend = Field(default_factory=Trend)
    notes: List[str] = Field(default_factory=list)


def get_analysis_json_schema() -> Dict[str, Any]:
    """Pydantic JSON Schema (dict) döndürür."""
    return AnalysisReport.model_json_schema()


