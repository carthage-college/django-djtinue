SELECT
    processors_contact.created_at,
    processors_contact.updated_at,
    processors_contact.salutation,
    processors_contact.first_name,
    processors_contact.second_name,
    processors_contact.last_name,
    processors_contact.previous_name,
    processors_contact.email,
    djtinue_enrichment_registration.email_work,
    processors_contact.phone,
    djtinue_enrichment_registration.phone_home,
    djtinue_enrichment_registration.phone_work,
    processors_contact.address1,
    processors_contact.address2,
    processors_contact.city,
    processors_contact.state,
    processors_contact.postal_code,
    djtinue_enrichment_registration.date_of_birth,
    djtinue_enrichment_registration.social_security_number,
    djtinue_enrichment_registration.social_security_four,
    djtinue_enrichment_registration.attended_before,
    djtinue_enrichment_registration.collegeid,
    djtinue_enrichment_registration.verify,
    processors_contact_order.order_id,
    processors_order.operator,
    processors_order.total,
    processors_order.cc_name,
    processors_order.cc_4_digits,
    processors_order.time_stamp,
    processors_order.status,
    processors_order.transid
FROM
    djtinue_enrichment_registration
LEFT JOIN
    processors_contact
ON
    djtinue_enrichment_registration.contact_ptr_id = processors_contact.id
LEFT JOIN
    processors_contact_order
ON
    processors_contact.id = processors_contact_order.contact_id
LEFT JOIN
    processors_order
ON
    processors_contact_order.order_id = processors_order.id

