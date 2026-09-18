create extension if not exists pgcrypto;

create table if not exists public.recipes (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  title text not null check (char_length(title) between 1 and 160),
  category text not null,
  prep_time text not null default '',
  image_url text,
  ingredients jsonb not null default '[]'::jsonb,
  steps jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.ratings (
  id uuid primary key default gen_random_uuid(),
  recipe_id uuid not null references public.recipes(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  value smallint not null check (value between 1 and 5),
  created_at timestamptz not null default now(),
  unique (recipe_id, user_id)
);

alter table public.recipes enable row level security;
alter table public.ratings enable row level security;

drop policy if exists "Anyone can read recipes" on public.recipes;
create policy "Anyone can read recipes" on public.recipes for select using (true);
drop policy if exists "Users create their own recipes" on public.recipes;
create policy "Users create their own recipes" on public.recipes for insert with check (auth.uid() = owner_id);
drop policy if exists "Owners update their recipes" on public.recipes;
create policy "Owners update their recipes" on public.recipes for update using (auth.uid() = owner_id) with check (auth.uid() = owner_id);
drop policy if exists "Owners delete their recipes" on public.recipes;
create policy "Owners delete their recipes" on public.recipes for delete using (auth.uid() = owner_id);

drop policy if exists "Anyone can read ratings" on public.ratings;
create policy "Anyone can read ratings" on public.ratings for select using (true);
drop policy if exists "Users create their own ratings" on public.ratings;
create policy "Users create their own ratings" on public.ratings for insert with check (auth.uid() = user_id);
drop policy if exists "Users update their own ratings" on public.ratings;
create policy "Users update their own ratings" on public.ratings for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

after insert on public.recipes;

-- In Supabase Storage, create a public bucket named recipe-images.
-- Use the authenticated user's id as the first folder in each object path.
