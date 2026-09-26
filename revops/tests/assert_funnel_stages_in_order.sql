-- Nenhuma etapa do funil pode acontecer antes da anterior.
-- Um cadastro depois do KYC ou um aporte antes do deal indicaria erro de join ou de dado.

select *

from {{ ref('fct_visitor_funnel') }}

where signed_up_at < first_seen_at
   or kyc_submitted_at < signed_up_at
   or kyc_approved_at < kyc_submitted_at
   or first_simulation_at < kyc_approved_at
   or first_deal_at < first_simulation_at
   or first_investment_at < first_deal_at
