import { useEffect, useMemo, useState } from 'react';

const categories = ['طبق رئيسي', 'حلويات', 'مشروبات', 'سلطات', 'فطور'];
const heroImage = 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1800&q=85';
const demo = [
  { id: '1', title: 'شاورما الدجاج', category: 'طبق رئيسي', time: '35 دقيقة', author: 'زائر', image: 'https://images.unsplash.com/photo-1559847844-5315695dadae?auto=format&fit=crop&w=1000&q=85', ingredients: ['دجاج', 'خبز', 'ثوم', 'مخلل'], steps: ['تبّل الدجاج', 'اشوه حتى ينضج', 'لفّه مع الخضار'], ratings: [5, 5, 4] },
  { id: '2', title: 'عصير المانجو', category: 'مشروبات', time: '10 دقائق', author: 'زائر', image: 'https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=1000&q=85', ingredients: ['مانجو', 'ماء', 'ثلج'], steps: ['قطّع المانجو', 'اخلط المكونات', 'قدّمه بارداً'], ratings: [5, 4, 5] },
];
const copy = {
  ar: { brand: 'بوابكا ريسيبتس', menu: 'الوصفات', add: 'أضف وصفتك', search: 'ابحث عن طبق أو مكوّن...', featured: 'وصفات من مطبخنا', intro: 'وصفات حقيقية، من أشخاص حقيقيين.', introText: 'شارك طبقك مع العالم. احفظ المكونات، اشرح طريقتك، ودع الآخرين يجربون ويقيّمون.', browse: 'استعرض الوصفات', ingredients: 'المكونات', steps: 'طريقة التحضير', category: 'التصنيف', time: 'وقت التحضير', title: 'اسم الطبق', image: 'رابط صورة الطبق', publish: 'نشر الطبق', update: 'تحديث الطبق', details: 'عرض الوصفة', rate: 'قيّم هذه الوصفة', settings: 'الإعدادات', language: 'اللغة', close: 'إغلاق', author: 'بواسطة', visitor: 'زائر', edit: 'تعديل', delete: 'حذف', developer: 'مبرمج الموقع', contact: 'للتواصل', noResults: 'لا توجد وصفات مطابقة.' },
  en: { brand: 'Boabca Recipes', menu: 'Recipes', add: 'Add your recipe', search: 'Search a dish or ingredient...', featured: 'From our kitchen', intro: 'Real recipes, from real people.', introText: 'Share your dish with the world. Save the ingredients, explain your method, and let others try and rate it.', browse: 'Browse recipes', ingredients: 'Ingredients', steps: 'Method', category: 'Category', time: 'Prep time', title: 'Dish name', image: 'Dish image URL', publish: 'Publish dish', update: 'Update dish', details: 'View recipe', rate: 'Rate this recipe', settings: 'Settings', language: 'Language', close: 'Close', author: 'By', visitor: 'Visitor', edit: 'Edit', delete: 'Delete', developer: 'Site developer', contact: 'Contact', noResults: 'No matching recipes.' },
};
const avg = (r) => r.ratings.length ? (r.ratings.reduce((a, b) => a + b, 0) / r.ratings.length).toFixed(1) : '0.0';
const uid = () => `${Date.now()}-${Math.random().toString(16).slice(2)}`;

function Stars({ value, onRate }) {
  return <span className="stars" aria-label={`${value} / 5`}>{[1, 2, 3, 4, 5].map((n) => <button type="button" key={n} className={n <= Math.round(value) ? 'star active' : 'star'} onClick={() => onRate?.(n)}>★</button>)}</span>;
}

export default function App() {
  const [lang, setLang] = useState(() => localStorage.boabcaLang || 'ar');
  const [recipes, setRecipes] = useState(() => { try { return JSON.parse(localStorage.boabcaRecipes || 'null') || demo; } catch { return demo; } });
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('all');
  const [selected, setSelected] = useState(null);
  const [settings, setSettings] = useState(false);
  const [editing, setEditing] = useState(null);
  const [ownerId] = useState(() => localStorage.boabcaVisitorId || (() => { const id = uid(); localStorage.boabcaVisitorId = id; return id; })());
  const t = copy[lang];
  const empty = { title: '', category: categories[0], time: '30 دقيقة', image: '', ingredients: '', steps: '' };
  const [form, setForm] = useState(empty);

  useEffect(() => { localStorage.boabcaLang = lang; document.documentElement.lang = lang; document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr'; }, [lang]);
  useEffect(() => { localStorage.boabcaRecipes = JSON.stringify(recipes); }, [recipes]);

  const shown = useMemo(() => recipes.filter((r) => (category === 'all' || r.category === category) && `${r.title} ${r.ingredients.join(' ')}`.toLowerCase().includes(query.toLowerCase())), [recipes, category, query]);
  const updateForm = (key, value) => setForm((old) => ({ ...old, [key]: value }));
  const scrollEditor = () => document.getElementById('editor')?.scrollIntoView({ behavior: 'smooth', block: 'start' });

  function saveRecipe(event) {
    event.preventDefault();
    const existing = editing && recipes.find((r) => r.id === editing);
    const recipe = { id: editing || uid(), title: form.title.trim(), category: form.category, time: form.time.trim(), image: form.image.trim() || heroImage, ingredients: form.ingredients.split('\n').map((x) => x.trim()).filter(Boolean), steps: form.steps.split('\n').map((x) => x.trim()).filter(Boolean), author: t.visitor, ownerId, ratings: existing?.ratings || [] };
    setRecipes((old) => editing ? old.map((r) => r.id === editing ? recipe : r) : [recipe, ...old]);
    setSelected(recipe); setEditing(null); setForm(empty);
  }
  function editRecipe(recipe) { setEditing(recipe.id); setForm({ title: recipe.title, category: recipe.category, time: recipe.time, image: recipe.image, ingredients: recipe.ingredients.join('\n'), steps: recipe.steps.join('\n') }); scrollEditor(); }
  function rateRecipe(id, rating) { setRecipes((old) => old.map((r) => r.id === id ? { ...r, ratings: [...r.ratings, rating] } : r)); setSelected((old) => old?.id === id ? { ...old, ratings: [...old.ratings, rating] } : old); }

  return <div className="site">
    <header className="nav wrap"><a className="wordmark" href="#top">BOABCA<span>RECIPES</span></a><nav><a href="#recipes">{t.menu}</a><a href="#about">{t.about || 'About'}</a><button className="pill" onClick={() => setSettings(true)}>⚙ {t.settings}</button></nav></header>
    <main id="top">
      <section className="hero wrap"><img src={heroImage} alt="Food" /><div className="hero-copy"><span className="eyebrow">✳ {t.featured} ✳</span><h1>{t.intro}</h1><p>{t.introText}</p><button className="cta" onClick={scrollEditor}>{t.add}</button></div></section>
      <section className="band yellow"><div className="band-inner"><span className="eyebrow">{t.featured}</span><h2>{lang === 'ar' ? 'اطبخ. شارك. كرّر.' : 'COOK. SHARE. REPEAT.'}</h2><button className="outline" onClick={() => document.getElementById('recipes')?.scrollIntoView({ behavior: 'smooth' })}>{t.browse} →</button></div></section>
      <section className="section wrap" id="recipes"><div className="section-head"><div><span className="eyebrow">✳ {t.menu} ✳</span><h2>{t.featured}</h2></div><div className="search-area"><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={t.search} /></div></div><div className="filters"><button className={category === 'all' ? 'filter active' : 'filter'} onClick={() => setCategory('all')}>{lang === 'ar' ? 'الكل' : 'All'}</button>{categories.map((c) => <button className={category === c ? 'filter active' : 'filter'} key={c} onClick={() => setCategory(c)}>{c}</button>)}</div><div className="recipe-grid">{shown.length ? shown.map((r) => <article className="recipe-card" key={r.id}><img src={r.image} alt={r.title} /><div className="recipe-info"><span className="badge">{r.category}</span><h3>{r.title}</h3><p>{t.author} {r.author} · {r.time}</p><div><Stars value={+avg(r)} /> <b>{avg(r)}</b> <small>({r.ratings.length})</small></div><div className="card-links"><button className="text-link" onClick={() => setSelected(r)}>{t.details} →</button>{r.ownerId === ownerId && <><button className="text-link" onClick={() => editRecipe(r)}>{t.edit}</button><button className="text-link danger" onClick={() => setRecipes((old) => old.filter((x) => x.id !== r.id))}>{t.delete}</button></>}</div></div></article>) : <p>{t.noResults}</p>}</div></section>
      <section className="band green"><div className="scattered"><span>Sear</span><span>Grill</span><span className="circled">Bake</span><span>Roast</span><span>Share</span></div></section>
      <section className="section editor-section wrap" id="editor"><div className="editor-intro"><span className="eyebrow">✳ {t.add} ✳</span><h2>{editing ? t.update : t.add}</h2><p>{t.introText}</p></div><form className="recipe-form" onSubmit={saveRecipe}><label>{t.title}<input required value={form.title} onChange={(e) => updateForm('title', e.target.value)} /></label><div className="form-row"><label>{t.category}<select value={form.category} onChange={(e) => updateForm('category', e.target.value)}>{categories.map((c) => <option key={c}>{c}</option>)}</select></label><label>{t.time}<input value={form.time} onChange={(e) => updateForm('time', e.target.value)} /></label></div><label>{t.ingredients}<textarea required rows="4" placeholder={lang === 'ar' ? 'مكوّن في كل سطر' : 'One ingredient per line'} value={form.ingredients} onChange={(e) => updateForm('ingredients', e.target.value)} /></label><label>{t.steps}<textarea required rows="4" placeholder={lang === 'ar' ? 'خطوة في كل سطر' : 'One step per line'} value={form.steps} onChange={(e) => updateForm('steps', e.target.value)} /></label><label>{t.image}<input type="url" value={form.image} onChange={(e) => updateForm('image', e.target.value)} placeholder="https://..." /></label><div><button className="cta">{editing ? t.update : t.publish}</button>{editing && <button type="button" className="outline cancel" onClick={() => { setEditing(null); setForm(empty); }}>{t.close}</button>}</div></form></section>
      <section className="band peach" id="about"><div className="split wrap"><div><span className="eyebrow">BOABCA AZEDDIN</span><h2>{lang === 'ar' ? 'وصفات تحفظها الذاكرة.' : 'Recipes worth remembering.'}</h2></div><p>{t.introText}</p></div></section>
    </main>
    <footer className="footer wrap"><strong>{t.developer}: BOABCA AZEDDIN</strong><a href="mailto:azeddinazeddin2005@gmail.com">{t.contact}: azeddinazeddin2005@gmail.com</a></footer>
    {selected && <div className="modal" onClick={() => setSelected(null)}><article className="detail" onClick={(e) => e.stopPropagation()}><button className="close" onClick={() => setSelected(null)}>×</button><img src={selected.image} alt={selected.title} /><span className="badge">{selected.category}</span><h2>{selected.title}</h2><Stars value={+avg(selected)} onRate={(v) => rateRecipe(selected.id, v)} /> <b>{avg(selected)} / 5</b><h3>{t.ingredients}</h3><ul>{selected.ingredients.map((x, i) => <li key={i}>{x}</li>)}</ul><h3>{t.steps}</h3><ol>{selected.steps.map((x, i) => <li key={i}>{x}</li>)}</ol><p>{t.rate}</p></article></div>}
    {settings && <div className="modal" onClick={() => setSettings(false)}><div className="settings" onClick={(e) => e.stopPropagation()}><h2>{t.settings}</h2><label>{t.language}<select value={lang} onChange={(e) => setLang(e.target.value)}><option value="ar">العربية</option><option value="en">English</option></select></label><button className="outline" onClick={() => setSettings(false)}>{t.close}</button></div></div>}
  </div>;
}
