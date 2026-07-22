-- bom-explode.sql — one BOM level for a single assembly, CandyCo NetSuite
-- =========================================================================
-- Used by the mrp-by-fg skill. The skill runs this ONCE PER assembly node,
-- substituting :parent_itemid, and does the multi-level recursion itself
-- (SuiteQL has no recursive CTE). See query-notes.md for the full method.
--
-- Returns the components on the ACTIVE, DEFAULT BOM of :parent_itemid:
--   * masterDefault = 'T'          -> the assembly's default BOM (skips
--                                     Rework/Convert/alternate BOMs)
--   * currentRevision              -> the authoritative active revision;
--                                     join components on THIS, not on
--                                     bomrevision effective-date math
--
-- CRITICAL — the `inactive` boolean on assemblyitembom renders as
-- 'No' / 'Yes' in this account (NOT 'T'/'F'), and `inactive = 'F'` matches
-- NOTHING, silently dropping every valid BOM. Never filter with `= 'F'`.
-- Exclude only explicitly-truthy values, defensively, across both
-- vocabularies. (masterDefault DOES render 'T'/'F' — the two booleans are
-- inconsistent, so each is handled on its own terms.)
-- =========================================================================

SELECT
    fg.itemid        AS parent_itemid,     -- the assembly we exploded
    fg.id            AS parent_id,
    c.item           AS component_id,      -- internal id of the component
    ci.itemid        AS component_itemid,  -- the displayed item number
    ci.itemtype      AS component_type,    -- 'Assembly' => recurse; else purchased leaf
    c.quantity       AS quantity,          -- qty of component per 1 of parent
    c.bomQuantity    AS bom_quantity,
    c.componentYield AS component_yield,
    c.lineId         AS line_id
FROM item fg
JOIN assemblyitembom      m  ON m.assembly    = fg.id
JOIN bomrevisioncomponent c  ON c.bomRevision = m.currentRevision
JOIN item                 ci ON ci.id         = c.item
WHERE fg.itemid = :parent_itemid
  AND m.masterDefault = 'T'
  AND (m.inactive IS NULL
       OR m.inactive NOT IN ('T', 'Yes', 'YES', 'yes', 'true', 'TRUE'))
ORDER BY c.lineId;

-- -------------------------------------------------------------------------
-- FG resolution (STEP 2 of the skill) — confirm the entered number exists
-- and is an assembly (only assemblies have BOMs):
--
--   SELECT id, itemid, itemtype FROM item WHERE itemid = :fg_item;
--
-- itemtype = 'Assembly' -> proceed. Anything else -> hard stop with a
-- clear message (a raw material / packaging item has no BOM to explode).
-- -------------------------------------------------------------------------
