# Policy rewrites — paste these in Shopify admin

I do not have the `write_legal_policies` permission, so these have to be pasted by hand:
**Settings → Policies**, then paste each one into the matching box.

## Why this matters more than it sounds

Your current policies are still written for the phone-case business and **contradict the store
you now have**:

- The **refund policy** says *"each tech accessory is custom-printed to order"*, *"all sales are
  final"*, *"we do not accept returns or exchanges"*, and tells buyers to double-check whether they
  ordered an iPhone 15 Pro or a Pro Max. Meanwhile every product page, the homepage trust bar and
  the product template all promise **7-day replacement** and Cash on Delivery.
  A customer in a dispute will screenshot that contradiction, and they will be right.
- The **shipping policy** quotes "United Kingdom: 2 to 4 business days" and "Rest of the World: 7
  to 15", with print-on-demand production times. Pakistan and COD are not mentioned anywhere.
- The **terms of service** reference Printify and print-on-demand fulfilment.
- **Contact** and **Legal notice** are UK-only, with no WhatsApp number.

Privacy policy is Shopify's standard text and is fine to leave as-is.

The rewritten Refund and Delivery text is in `refund-policy.html` and `shipping-policy.html`.
Both keep the Aura Group Ventures Ltd registration details, which you are required to show, but
make the operational terms match how the store actually runs.

## Terms of service — the two edits that matter

Rather than rewriting the whole thing, fix these in the existing text:

1. **Section 5** currently says products are *"custom-manufactured on a made-to-order basis via
   print-on-demand fulfillment"*. Replace with: *"Products are sourced from our supplier network in
   Pakistan and dispatched from local warehouses. Product images are supplied by the manufacturer;
   slight variation in colour or finish is possible."*
2. **Section 7** names **Printify** as a third-party tool. That app is being removed. Replace
   "Printify" with "our fulfilment and courier partners".

Also worth adding to Section 6: *"Orders are confirmed by phone or WhatsApp before dispatch.
Orders we cannot confirm after reasonable attempts may be cancelled."* That single line is what
lets you cancel unconfirmable COD orders without argument.

## Contact page

The existing Contact policy is accurate but incomplete for Pakistan. Add above the UK details:

> **Customer support, Pakistan**
> WhatsApp: +92 305 3488833 (9am to 9pm, every day) — fastest way to reach us
> Email: support@wiredandwarped.com
> We reply to WhatsApp within a couple of hours during opening times.

Keep the UK corporate block underneath. It is a legal requirement, not a selling point, so it
belongs below the number customers actually use.
