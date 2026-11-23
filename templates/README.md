# 输入与记录模板

[intake.md](intake.md)是初次输入卡；CSV只有字段表头，不含真实数据。

- companies.csv：一行一公司，保留company_id与原主表ID；集团独立采购主体可分开。
- contacts.csv：一行一个联系方式记录，使用contact_id、person_id和company_id关联，避免多人、多邮箱或号码混在一个值中。采购职位和本人渠道归属分别标记。
- evidence.csv：一行一证据，关联record_id和支持的字段；多来源不能仅计页面数，要判断是否独立。
- channel-costs.csv：一行一渠道/费用记录，实际与未知费用分开。新公司归因只计一次，其他渠道另计补证贡献。

已有主表能表达这些信息时直接映射，缺字段再补，不强制换表。用户产出的真实数据不提交到公开仓库。
