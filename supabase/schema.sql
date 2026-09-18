-- Shared dishes and ratings for the Maida community app.
create extension if not exists pgcrypto;

create table if not exists public.dishes (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 120),
  category text not null check (category in ('dishes', 'desserts', 'fast', 'drinks')),
  description text not null default '',
  image_url text,
  quantity integer not null default 100 check (quantity >= 100),
  calories numeric not null default 0,
  protein numeric not null default 0,
  carbs numeric not null default 0,
  fat numeric not null default 0,
  fiber numeric not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.dish_ratings (
  id uuid primary key default gen_random_uuid(),
  dish_id uuid not null references public.dishes(id) on delete cascade,
  voter_id text not null,
  value smallint not null check (value between 1 and 5),
  created_at timestamptz not null default now(),
  unique (dish_id, voter_id)
);

alter table public.dishes enable row level security;
alter table public.dish_ratings enable row level security;

drop policy if exists "Anyone can read dishes" on public.dishes;
create policy "Anyone can read dishes" on public.dishes for select using (true);
drop policy if exists "Anyone can add dishes" on public.dishes;
create policy "Anyone can add dishes" on public.dishes for insert with check (true);
drop policy if exists "Anyone can update dishes" on public.dishes;
create policy "Anyone can update dishes" on public.dishes for update using (true) with check (true);
drop policy if exists "Anyone can delete dishes" on public.dishes;
create policy "Anyone can delete dishes" on public.dishes for delete using (true);

drop policy if exists "Anyone can read dish ratings" on public.dish_ratings;
create policy "Anyone can read dish ratings" on public.dish_ratings for select using (true);
drop policy if exists "Anyone can rate dishes" on public.dish_ratings;
create policy "Anyone can rate dishes" on public.dish_ratings for insert with check (true);
drop policy if exists "Anyone can change a rating" on public.dish_ratings;
create policy "Anyone can change a rating" on public.dish_ratings for update using (true) with check (true);

grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on public.dishes to anon, authenticated;
grant select, insert, update on public.dish_ratings to anon, authenticated;
