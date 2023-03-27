SELECT 
     a.uuid,
     u.display_name,
     u.handle,
     a.message,
     a.created_at,
     a.expires_at
FROM public.activities a
INNER JOIN public.users u
ON a.user_uuid = u.uuid
WHERE 
    a.uuid = %(uuid)s