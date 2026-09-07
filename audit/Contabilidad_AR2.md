I’ll trace the accounting flow end to end—accounts, journal creation/posting, document mappings, period closing, and inventory/fiscal boundaries—then report concrete findings with file and line references.

/ Search (glob)
  │ "**/*"
  └ 330 files found

● Inspect repository status and recent commits (shell)
  │ git status --short; git --no-pager log -5 --oneline
  └ 18 lines…

● Read Contabilidad_AR2.md
  └ audit\Contabilidad_AR2.md

/ Search (glob)
  │ "inventory/**/*.py"
  └ 15 files found

/ Search (glob)
  │ "fiscal/**/*.py"
  └ 75 files found

/ Search (glob)
  │ "sales/**/*.py"
  └ 20 files found

/ Search (glob)
  │ "accounting/**/*.py"
  └ 51 files found

/ Search (grep)
  │ "(Journal|Entry|Asiento|ledger|contab|post|closing|period|cierre|inventory|fiscal|tax)" in *.py
  │ (accounting, inventory, fiscal, sales, purchases)
  └ 108 files found

● Read period.py
  │ accounting\models\period.py
  └ 44 lines read

● Read account.py
  │ accounting\models\account.py
  └ 81 lines read

● Read generate_entry.py
  │ accounting\services\generate_entry.py
  └ 103 lines read

● Read integration.py
  │ accounting\integration.py
  └ 177 lines read

● Read journal.py
  │ accounting\models\journal.py
  └ 96 lines read

● Read ledger.py
  │ accounting\views\ledger.py
  └ 41 lines read

● Read journal.py
  │ accounting\forms\journal.py
  └ 25 lines read

● Read journal.py
  │ accounting\views\journal.py
  └ 67 lines read

● Read trial_balance.py
  │ accounting\views\trial_balance.py
  └ 39 lines read

● Read balance_sheet.py
  │ accounting\views\balance_sheet.py
  └ 44 lines read

● Read load_chart_of_accounts_full.py
  │ accounting\management\commands\load_chart_of_accounts_full.py
  └ 186 lines read

● Read create_fiscal_year.py
  │ accounting\management\commands\create_fiscal_year.py
  └ 58 lines read

The core accounting model already shows several high-risk consistency gaps (entry validation timing, period status API, and account-code mismatches). I’m now cross-checking those against purchase, sale, inventory, and fiscal invoice lifecycles so the audit distinguishes isolated defects from systemic posting failures.

● Read period.py
  │ accounting\models\period.py
  └ L1:120 (44 lines read)

● Read integration.py
  │ inventory\integration.py
  └ 121 lines read

● Read account_movement.py
  │ accounting\models\account_movement.py
  └ 44 lines read

● Read models.py
  │ inventory\models.py
  └ 75 lines read

● Read purchase.py
  │ purchases\models\purchase.py
  └ 265 lines read

● Read purchase.py
  │ purchases\views\purchase.py
  └ 237 lines read

● Read sale.py
  │ sales\models\sale.py
  └ 64 lines read

● Read sale_item.py
  │ sales\models\sale_item.py
  └ 70 lines read

● Read sales.py
  │ sales\views\sales.py
  └ 136 lines read

● Read fiscal_invoice.py
  │ fiscal\models\fiscal_invoice.py
  └ 206 lines read

● Read fiscal_invoice_line.py
  │ fiscal\models\fiscal_invoice_line.py
  └ 42 lines read

● Read tax.py
  │ fiscal\models\tax.py
  └ 51 lines read

● Read tests.py
  │ accounting\tests.py
  └ 3 lines read

● Read fiscalinvoice_finalize.py
  │ fiscal\views\fiscalinvoice_finalize.py
  └ 121 lines read

● Read fiscal_invoice.py
  │ fiscal\views\fiscal_invoice.py
  └ 86 lines read

● Read 0002_initial.py
  │ accounting\migrations\0002_initial.py
  └ 76 lines read

● Read fiscal_invoice_line.py
  │ fiscal\views\fiscal_invoice_line.py
  └ 102 lines read

● Read 0003_accountmovement.py
  │ accounting\migrations\0003_accountmovement.py
  └ 86 lines read

● Read 0005_inventorymovement_internal_tax.py
  │ inventory\migrations\0005_inventorymovement_internal_tax.py
  └ 20 lines read

/ Search (grep)
  │ "generate_accounting_entry|create_.*journal|JournalEntry|close|CLOSED|LOCKED|is_closed|is_locked
  │ |get_current" in *.py
  └ 133 lines found

● Read __init__.py
  │ accounting\models\__init__.py
  └ 3 lines read

● Read 0001_initial.py
  │ accounting\migrations\0001_initial.py
  └ 77 lines read

● Read account.py
  │ accounting\views\account.py
  └ L120:210 (58 lines read)

● Read fiscal_invoice_line.py
  │ fiscal\forms\fiscal_invoice_line.py
  └ 29 lines read

● Read urls.py
  │ accounting\urls.py
  └ 60 lines read

● Read load_chart.py
  │ accounting\management\commands\load_chart.py
  └ 150 lines read

● Read load_chart_of_accounts_full.py
  │ accounting\management\commands\load_chart_of_accounts_full.py
  └ L1:40 (40 lines read)

/ Search (grep)
  │ "JournalEntry.objects.create|JournalEntryLine.objects.create|Period.objects.get_current|is_close
  │ d|is_locked|status="OPEN"" in *.py
  └ 52 lines found

/ Search (grep)
  │ "get_account\(company, "[^"]+"\)|account_code\s*=\s*"[^"]+"" in *.py
  └ 10 lines found

● Run accounting integration tests (shell)
  │ & .\.venv\Scripts\python.exe manage.py test accounting inventory fiscal sales purchases
  │ --noinput
  └ 2 lines…

● Run Django system checks (shell)
  │ & .\.venv\Scripts\python.exe manage.py check
  └ 2 lines…

● Review current accounting-related worktree changes (shell)
  │ git --no-pager diff -- accounting inventory fiscal purchases sales | Select-Object -First 400
  └ 401 lines…

● Collect audit-relevant line references (shell)
  │ $files=@('accounting\models\journal.py','accounting\models\period.py','accounting\integration.
  │ py','accounting\services\generate_entry.py','accounting\views\journal.py','accounting\views\ac
  │ count.py','purchases\views\purchase.py','inventory\integration.py','sales\views\sales.py','fis
  │ cal\models\fiscal_invoice.py','fiscal\views\fiscalinvoice_finalize.py','fiscal\models\fiscal_i
  │ nvoice_line.py','accounting\management\commands\load_chart.py','accounting\management\commands…
  └ 405 lines…

/ Search (grep)
  │ "fiscalinvoice_finalize|finalize\(" in *.py
  └ 7 lines found

● Read complete audit targets with line numbers (shell)
  │ $files=@('accounting\views\balance_sheet.py','accounting\views\account.py','accounting\models\
  │ journal.py','accounting\integration.py','accounting\services\generate_entry.py','purchases\mod
  │ els\purchase.py','sales\models\sale.py','inventory\integration.py','fiscal\models\fiscal_invoi
  │ ce.py','fiscal\views\fiscal_invoice.py','fiscal\views\fiscalinvoice_finalize.py'); foreach($f
  │ in $files){Write-Output "--- $f"; $i=0; Get-Content $f | ForEach-Object { $i++; "{0}: {1}" -f …
  └ 20 lines…

/ Search (grep)
  │ "update_inventory_from_purchase|create_purchase_journal_entry|purchase.calculate_totals|update_i
  │ nventory_from_sale|create_sale_journal_entry|create_cmv_journal_entry|delete_journal_entries|rev
  │ ert_inventory" (purchases\views\purchase.py)
  └ 10 lines found

/ Search (grep)
  │ "acc_inventory|acc_iva_credit|acc_prov|acc_clients|acc_sales|acc_iva_debit|acc_cmv|JournalEntry.
  │ objects.create|date=timezone.now|sale\.vat_amount|sale\.cost_total" (accounting\integration.py)
  └ 25 lines found

/ Search (grep)
  │ "def balance_sheet_view|bal =|Period.objects.filter|period =
  │ get_object_or_404|period.status|entry.save|formset.save|if not entry.is_balanced" in *.py
  │ (accounting)
  └ 13 lines found

/ Search (grep)
  │ "get\(|product_cost|unit_cost|quantity -=|return$|InventoryItem.objects.get"
  │ (inventory\integration.py)
  └ 6 lines found

/ Search (grep)
  │ "def finalize|calculate_totals|self\.total_amount|self\.is_closed|FiscalInvoice.objects.create|s
  │ ale_id" in *.py (fiscal)
  └ 29 lines found

## Audit conclusion

The accounting module is **not currently reliable for production double-entry accounting**. Manual journal creation fails, automated purchase/sale postings are not persistently linked to periods or users, several integrations reference nonexistent fields or incompatible account codes, and fiscal invoices are not consistently posted to the ledger. Period closing is also reversible and insufficiently controlled.

### Findings

| # | Severity | Area | Location | Finding / impact |
|---|---|---|---|---|
| 1 | **Critical** | Journal posting | `accounting/models/journal.py:49-64` | `JournalEntry.clean()` calls nonexistent `period.is_closed` and `period.is_locked` attributes. Any save with a valid period can raise `AttributeError`. Automated entries also omit the required `period` and `created_by` fields. |
| 2 | **Critical** | Journal posting | `accounting/views/journal.py:49-55` | The journal header is saved before its lines. Balance validation therefore occurs before the formset is persisted; `JournalEntry.save()` cannot validate the completed entry. The subsequent line saves do not invoke `full_clean()`, so invalid or unbalanced entries can be persisted. |
| 3 | **Critical** | Sales integration | `accounting/integration.py:75-94` | The posting uses `sale.vat_amount`, but the model defines `iva_amount` (`sales/models/sale.py:21-25`). Sale posting therefore fails with `AttributeError`. CMV posting similarly uses nonexistent `sale.cost_total` instead of `total_cost` (`accounting/integration.py:114-128`). |
| 4 | **Critical** | Purchase/sale integration | `accounting/integration.py:35-58`, `75-128` | Automated entries create `JournalEntry` objects without `period` or `created_by`, despite both being non-nullable. They also use `timezone.now()` instead of the source document date, so postings can fall into the wrong accounting period. |
| 5 | **High** | Chart of accounts | `accounting/management/commands/load_chart.py`, `load_chart_of_accounts_full.py` | Two incompatible charts exist. One uses codes such as `1.1.09`, `2.1.01`, `4.1.01`; the “full” loader uses `1.1.8`, `2.1.1`, `4.1.1`. Existing integrations use both formats. Re-running or selecting a different loader can make posting fail with `Account.DoesNotExist`. |
| 6 | **High** | Argentine tax accounting | `accounting/integration.py:41-43`, `81-83` | Tax mappings are inconsistent with the chart definitions. In the full chart, `7.2` is “Income Tax,” but purchase VAT credit is posted there. Sales VAT is posted to aggregate account `7.1`, rather than a dedicated IVA Débito Fiscal account. This can materially misstate IVA positions and tax liabilities. |
| 7 | **High** | Purchase document mapping | `accounting/integration.py:45-58`, `purchases/models/purchase.py:117-138` | Purchase line `expense_account` is ignored; every purchase is debited to inventory. Perceptions and retentions are included in `Purchase.total_amount`, but no corresponding ledger lines are generated. Any purchase with perceptions or retentions is unbalanced: debit = net + VAT, credit = net + VAT + perceptions − retentions. |
| 8 | **High** | Fiscal integration | `fiscal/views/fiscal_invoice.py:18-55`, `accounting/services/generate_entry.py:13-37` | A fiscal invoice is created from a sale but has no foreign key back to the sale and does not copy sale lines. Finalization does not invoke accounting posting. The separate generator uses nonexistent account codes `"CAJA"` and `"VENTAS"` and calls `Period.objects.get_current(company)`, but `Period` defines no such manager method. |
| 9 | **High** | Inventory / CMV | `inventory/integration.py:50-79` | Sale inventory processing can raise `InventoryItem.DoesNotExist` after the sale item has already been saved. No stock availability check prevents negative inventory. `InventoryItem` has no `product_cost` field, so `getattr(inv_item, "product_cost", 0)` produces zero cost and can generate zero CMV. |
| 10 | **High** | Transactional consistency | `purchases/views/purchase.py:130-140`, `sales/views/sales.py:92-108` | Purchase persistence is atomic only through purchase/formsets; inventory, journal, and account-current updates occur afterward and outside the transaction. Sales perform reversal and reposting as separate operations without `transaction.atomic()`. Partial failures can leave stock, subledger, and general ledger out of sync. |
| 11 | **High** | Period management | `accounting/views/account.py:134-176` | Period queries use `Period.objects.filter(company=company)` and `get_object_or_404(..., company=company)`, but `Period` has no `company` field; the company is reached through `fiscal_year__company`. Period listing and open/close/lock endpoints therefore fail at runtime. |
| 12 | **High** | Period closing | `accounting/views/account.py:145-176` | Closing and locking are unrestricted state assignments. There is no HTTP method restriction, permission requirement, validation that entries are balanced, reconciliation, fiscal-year status handling, or closing-entry generation. A locked period can also be reopened through the open endpoint. |
| 13 | **High** | Financial reporting | `accounting/views/balance_sheet.py:21` | `Account.balance` is a property, but the view calls `acc.balance(company)`, causing a `TypeError`. The balance sheet is therefore nonfunctional. |
| 14 | **Medium** | Audit trail | `accounting/integration.py:60-68`, `100-108`, `134-142` | Source-document linkage is encoded only in description text and deletions use `description__icontains`. This is not idempotent and can delete unrelated entries with the same invoice/sale number. Accounting corrections should use source IDs and reversal entries, not destructive deletion. |
| 15 | **Medium** | Chart controls | `accounting/models/account.py:36-44` | Account validation checks numeric code segments and parent existence, but does not enforce same-company parent ownership, prevent cycles, prevent posting to group accounts, or prevent account-type inconsistencies in the hierarchy. |

### Double-entry assessment

The intended purchase and sale formulas are balanced only in the simplest case:

- Purchase: `Inventory + VAT = Supplier`
- Sale: `Receivable = Sales + IVA`
- CMV: `CMV = Inventory`

However, those formulas are not executable as implemented because of missing required journal fields, nonexistent model attributes, incompatible account codes, and absent period resolution. Purchase perceptions/retentions and other fiscal components are not represented in the journal, so the ledger cannot reconcile to fiscal totals.

### Argentine-practice gaps

The current design does not provide the controls normally expected for Argentine bookkeeping:

- No immutable source-document-to-asiento relationship.
- No controlled numbering or journal type/point-of-sale metadata on accounting entries.
- No proper IVA débito/crédito, perceptions, retentions, IIBB, Ganancias, and SUSS posting matrix.
- No closing entries transferring income/expense results to the appropriate equity/result account.
- No fiscal-year closing workflow.
- No formal correction/reversal mechanism.
- Posting date is not consistently the document date.
- No reconciliation between AFIP fiscal totals, subledgers, inventory valuation, and the general ledger.
- Fiscal invoice finalization and CAE approval are not coupled to successful accounting posting.

### Recommended remediation order

1. Repair the journal domain model: period resolution, user/source fields, atomic header-plus-lines creation, decimal validation, and database-level debit/credit constraints.
2. Establish one canonical chart of accounts and replace hard-coded strings with validated account configuration.
3. Implement document-linked, idempotent posting services for purchases, sales, fiscal invoices, VAT, perceptions, retentions, inventory, and CMV.
4. Make inventory, subledger, fiscal document, and ledger updates one atomic workflow with explicit reversal handling.
5. Implement controlled period closing and fiscal-year closing, including result transfer and locking that cannot be bypassed.
6. Add reconciliation tests covering ordinary VAT, exempt/non-taxed sales, perceptions, retentions, inventory cost, closed periods, duplicate posting, and failed integration rollback.

Runtime Django checks/tests could not be executed because the repository’s `.venv` launcher points to a missing Python installation, so the findings above are based on static inspection of the current worktree.

