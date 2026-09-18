# ربط Supabase

تمت إضافة عميل Supabase ومخطط قاعدة البيانات إلى المشروع.

## المطلوب منك مرة واحدة

1. أنشئ مشروعًا في https://supabase.com/dashboard.
2. من **SQL Editor** شغّل كامل الملف `supabase/schema.sql`.
3. من **Storage** أنشئ bucket عامًا باسم `recipe-images`.
4. من **Authentication > Providers** فعّل Google وأضف إعدادات Google OAuth.
5. من إعدادات المشروع انسخ **Project URL** و**Publishable/Anon key**.
6. أضفهما إلى GitHub Repository Secrets بالاسمين:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`

لا تشارك `service_role key` ولا تضعه في الواجهة.

بعد تزويدي بـ Project URL وAnon key (ويمكنك إخفاء أي مفاتيح سرية أخرى)، أستطيع إكمال تحويل مكونات الواجهة من `localStorage` إلى الوصفات والتقييمات والحسابات المشتركة فعليًا.
