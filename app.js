const API_BASE = window.location.origin; // assume same host
let CONFIG = {
  asset_base_url: '',
  page_size: 60,
  redis_enabled: false,
  list_mode: 'infinite',
  announce_enabled: false,
  ads_enabled: false,
  ads: [],
  old_blacklist_migrate_enabled: false,
};

const SITE_TITLE_ZH = 'AI绘画咒语图库 : AI TAG Prompt Art Gallery';
const SITE_TITLE_EN = 'AI TAG Prompt Art Gallery';
const HOME_DESC_ZH = '专为 Stable Diffusion Web UI、ComfyUI 及 NovelAI 用户打造。在这里，您可以一键搜索海量作品与“咒语”参数，参考优秀范例，让 AI 绘画学习变得更简单高效';
const HOME_DESC_EN = 'Built for Stable Diffusion, ComfyUI, and NovelAI. Search a vast library of images and prompts with one click. Reference top-tier examples to streamline your workflow and master AI art faster.';

function getLangParamRaw() {
  try {
    const url = new URL(window.location.href);
    return String(url.searchParams.get('lang') || '').trim().toLowerCase();
  } catch {
    return '';
  }
}
function normalizeLangFromParam(raw) {
  const v = String(raw || '').trim().toLowerCase();
  if (v === 'us') return 'en';
  if (v === 'cn' || v === 'zh') return 'zh';
  return '';
}
function detectBrowserLang() {
  try {
    const list = Array.isArray(navigator.languages) && navigator.languages.length ? navigator.languages : [navigator.language];
    const joined = list.map((x) => String(x || '').toLowerCase()).join(',');
    return joined.includes('zh') ? 'zh' : 'en';
  } catch {
    return 'en';
  }
}
const LANG_PARAM_RAW = getLangParamRaw();
const CURRENT_LANG = normalizeLangFromParam(LANG_PARAM_RAW) || detectBrowserLang();
try { window.GALLERY_LANG = CURRENT_LANG; } catch { }

const I18N = {
  zh: {
    search_placeholder_q: '搜索:作品id/作者id/简介/tags(日文)/投稿日期/AI类型/模型(支持 -排除 与 OR 双引号精准)',
    search_placeholder_prompt: '搜索:NAI和SD AI元数据Prompt(不含负面词和ComfyUI)',
    sort_label: '排序',
    sort_new: '新作品排序',
    sort_monthly: '每月排行榜',
    time_range_label: '时间范围',
    time_all: '全部时间',
    time_full_year: ({ year }) => `${year}全年`,
    time_quarter: ({ year, quarter }) => `${year}第${quarter}季度`,
    time_older: '更老(2023年9月之前)',
    time_current_month: '当前月份',
    btn_search: '搜索',
    blacklist_placeholder: '黑名单屏蔽关键词(逗号/空格分隔,不屏蔽AI元数据)',
    btn_save_blacklist: '保存黑名单',
    status_searching: '搜索中…',
    no_results: '无搜索结果',
    loading: '载入中…',
    loading_failed: '载入失败',
    rank_processing: '排行榜正在处理中，请等待2小时后查看',
    load_more: '加载更多',
    jump_label: '跳至第',
	    jump_placeholder: '页码',
	    btn_go: '跳转',
	    open_work_new_window: '新窗口打开作品',
	    show_suspect_invalid_tags: '显示疑似无效TAG作品',
	    show_naix_invalid_tags: '显示NAI_X无效TAG作品',
	    fc_chip_label: '设置与页码',
    fc_q_placeholder: '搜索：id/作者id/简介/tags/日期/类型/模型',
    fc_prompt_placeholder: '搜索：NAI/SD元数据Prompt',
    fc_blacklist_placeholder: '黑名单屏蔽关键词(逗号/空格分隔)',
    preview_alt: '预览',
    back_btn: '← 返回',
    detail_header: '作品详情',
    home_alt: '首页',
    home_title: '返回首页',
    thumb_alt: '缩略图',
    type_search_tip: '点击按类型搜索',
    naix_suspect: '疑无效TAG',
    naix_suspect_bracket: '[疑无效TAG]',
    naix_suspect_paren: '（疑无效TAG）',
    non_standard_format: '非标准格式',
    non_standard_format_bracket: '[非标准格式]',
    non_standard_format_paren: '（非标准格式）',
    non_standard_format_tip: '这是来自 tensor.art 网址在线生成流，并非正确的 ComfyUI 工作流',
    work_fallback: ({ id }) => `作品 ${id}`,
    images_count: ({ n }) => `${n} 张`,
    err_network: '网络错误',
    show_full_meta: '显示完整 AI 元数据',
    dm_pixiv_id: 'Pixiv ID',
    dm_author: '作者',
    dm_type: '类型',
    dm_tags: '标签',
    dm_caption: '作品简介',
    dm_posted_at: '投稿时间',
    dm_unknown: '未知',
    dm_none: '无',
    dm_views: '浏览',
    dm_bookmarks: '收藏',
    caption_show_all: '显示全部简介',
    caption_collapse: '折叠简介',
    ai_meta_mode: 'AI元数据模式',
    copy_json: '复制 JSON',
    copy_instruction: '复制指令',
    copied: '已复制',
    copy_failed: '复制失败',
    copy_failed_manual: '复制失败，请手动复制:\n\n',
    show_all: '显示全部',
    collapse: '折叠',
    copy_all_image_links: '复制全部图片链接',
    no_links_to_copy: '无可复制链接',
    copied_n_links: ({ n }) => `已复制 ${n} 条链接`,
    copy_failed_popup: '复制失败，已弹出文本',
    prev_group: '上一组',
    next_group: '下一组',
    seo_tags_prefix: '标签',
    seo_ai_meta_prefix: 'AI元数据',
    announce_title: '公告说明',
    announce_close: '关闭',
    announce_p1: '这网站是收集P站AI图带AI元数据作品',
    announce_p2: '初哀是方便大家新手学习或更加简单方便抄作业玩AI绘画',
    announce_p3: '我自己也经常分享自己图给群友们，还从24年开始使用自己每月25刀购买NAI号搭建AI机器人给群友们免费玩',
    announce_p4: '当然我也能理解作者们花时间来创作作品的劳动成果',
    announce_strong_prefix: '所以如果不想公开自己作品，随时都可以',
    announce_strong_link: 'P站联系我(Puid:120618272)',
    announce_strong_suffix: '删除',
    lang_btn_zh: '中文',
    lang_btn_en: 'EN',
    btn_import_blacklist: '导入旧域名黑名单',
    import_blacklist_popup_blocked: '弹窗被浏览器拦截，请允许本站弹窗后再点一次',
    import_blacklist_starting: '正在从旧域名导入…',
    import_blacklist_done: '已导入旧域名黑名单',
    import_blacklist_failed: '导入失败（可能旧域名禁止被 iframe 嵌入或无旧数据）',
  },
  en: {
    search_placeholder_q: 'Search: work id / author id / caption / tags / date / AI type / model (supports -exclude, OR, and quoted exact match)',
    search_placeholder_prompt: 'Search: NAI & SD AI metadata prompt (no negative / no ComfyUI)',
    sort_label: 'Sort',
    sort_new: 'Newest',
    sort_monthly: 'Monthly ranking',
    time_range_label: 'Time range',
    time_all: 'All time',
    time_full_year: ({ year }) => `${year} (full year)`,
    time_quarter: ({ year, quarter }) => `${year} Q${quarter}`,
    time_older: 'Older (before 2023-09)',
    time_current_month: 'Current month',
    btn_search: 'Search',
    blacklist_placeholder: 'Block keywords (comma/space separated; does not block AI metadata)',
    btn_save_blacklist: 'Save blocklist',
    status_searching: 'Searching…',
    no_results: 'No results',
    loading: 'Loading…',
    loading_failed: 'Load failed',
    rank_processing: 'The ranking is being processed. Please check again after 2 hours.',
    load_more: 'Load more',
    jump_label: 'Go to',
	    jump_placeholder: 'Page',
	    btn_go: 'Go',
	    open_work_new_window: 'Open works in a new window',
	    show_suspect_invalid_tags: 'Show suspect invalid-tag works',
	    show_naix_invalid_tags: 'Show NAI_X invalid-tag works',
	    fc_chip_label: 'Settings & page',
    fc_q_placeholder: 'Search: id / author / caption / tags / date / type / model',
    fc_prompt_placeholder: 'Search: NAI/SD metadata prompt',
    fc_blacklist_placeholder: 'Block keywords (comma/space separated)',
    preview_alt: 'Preview',
    back_btn: '← Back',
    detail_header: 'Work details',
    home_alt: 'Home',
    home_title: 'Back to home',
    thumb_alt: 'Thumbnail',
    type_search_tip: 'Search by type',
    naix_suspect: 'Suspect invalid tags',
    naix_suspect_bracket: '[Suspect invalid tags]',
    naix_suspect_paren: '(Suspect invalid tags)',
    non_standard_format: 'Non-standard format',
    non_standard_format_bracket: '[Non-standard format]',
    non_standard_format_paren: '(Non-standard format)',
    non_standard_format_tip: 'Generated from tensor.art online workflow; not a proper ComfyUI workflow.',
    work_fallback: ({ id }) => `Work ${id}`,
    images_count: ({ n }) => `${n} images`,
    err_network: 'Network error',
    dm_pixiv_id: 'Pixiv ID',
    dm_author: 'Author',
    dm_type: 'Type',
    dm_tags: 'Tags',
    dm_caption: 'Caption',
    dm_posted_at: 'Posted at',
    dm_unknown: 'Unknown',
    dm_none: 'None',
    dm_views: 'Views',
    dm_bookmarks: 'Bookmarks',
    caption_show_all: 'Show full caption',
    caption_collapse: 'Collapse caption',
    ai_meta_mode: 'AI metadata mode',
    copy_json: 'Copy JSON',
    copy_instruction: 'Copy instruction',
    copied: 'Copied',
    copy_failed: 'Copy failed',
    copy_failed_manual: 'Copy failed. Please copy manually:\n\n',
    show_all: 'Show all',
    collapse: 'Collapse',
    copy_all_image_links: 'Copy all image links',
    no_links_to_copy: 'No links to copy',
    copied_n_links: ({ n }) => `Copied ${n} links`,
    copy_failed_popup: 'Copy failed; opened as text',
    prev_group: 'Prev',
    next_group: 'Next',
    seo_tags_prefix: 'Tags',
    seo_ai_meta_prefix: 'AI metadata',
    announce_title: 'Announcement',
    announce_close: 'Close',
    announce_p1: 'This site collects Pixiv AI works that include AI metadata.',
    announce_p2: 'The goal is to help beginners learn faster and make it easier to study good prompts and settings.',
    announce_p3: 'I also often share my own works with group friends. Since 2024, I have been paying $25/month for a NovelAI account to run an AI bot for group friends to use for free.',
    announce_p4: 'I also understand the effort creators put into making their works.',
    announce_strong_prefix: 'If you do not want your works to be public, you can message me on Pixiv anytime to have them removed:',
    announce_strong_link: 'Message me on Pixiv (Puid:120618272)',
    announce_strong_suffix: '',
    lang_btn_zh: 'ZH',
    lang_btn_en: 'EN',
    btn_import_blacklist: 'Import old blocklist',
    import_blacklist_popup_blocked: 'Popup was blocked. Please allow popups and retry.',
    import_blacklist_starting: 'Importing from old domain…',
    import_blacklist_done: 'Imported old blocklist',
    import_blacklist_failed: 'Import failed (old domain may block iframe or no data)',
  },
};
function t(key, vars = {}) {
  const dict = I18N[CURRENT_LANG] || I18N.zh;
  const val = dict[key];
  if (typeof val === 'function') return String(val(vars));
  if (val == null) return String(key);
  return String(val);
}
function withLangParam(urlOrPath) {
  if (!LANG_PARAM_RAW) return String(urlOrPath || '');
  const raw = String(urlOrPath || '');
  try {
    const u = new URL(raw, window.location.origin);
    if (u.origin === window.location.origin) {
      u.searchParams.set('lang', LANG_PARAM_RAW);
      return u.pathname + u.search + u.hash;
    }
    return raw;
  } catch {
    return raw;
  }
}

function applyStaticI18n() {
  try {
    document.documentElement.lang = (CURRENT_LANG === 'zh') ? 'zh-CN' : 'en';
  } catch { }
  try {
    const homeLink = document.getElementById('homeLink');
    const homeImg = homeLink ? homeLink.querySelector('img') : null;
    if (homeLink) homeLink.href = withLangParam('/');
    if (homeLink) homeLink.title = t('home_title');
    if (homeImg) homeImg.alt = t('home_alt');
  } catch { }
  try { if (qInput) qInput.placeholder = t('search_placeholder_q'); } catch { }
  try { if (promptInput) promptInput.placeholder = t('search_placeholder_prompt'); } catch { }
  try { if (blacklistInput) blacklistInput.placeholder = t('blacklist_placeholder'); } catch { }
  try { if (searchBtn) searchBtn.textContent = t('btn_search'); } catch { }
  try { if (saveBlacklistBtn) saveBlacklistBtn.textContent = t('btn_save_blacklist'); } catch { }
  try { if (importOldBlacklistBtn) importOldBlacklistBtn.textContent = t('btn_import_blacklist'); } catch { }
  try {
    document.querySelectorAll('#searchStatus span').forEach((n) => { n.textContent = t('status_searching'); });
  } catch { }
  try { if (noResultEl) noResultEl.textContent = t('no_results'); } catch { }
  try { if (loadMoreBtn) loadMoreBtn.textContent = t('load_more'); } catch { }
  try { if (sortModeSel) sortModeSel.setAttribute('aria-label', t('sort_label')); } catch { }
  try { if (timeRangeSel) timeRangeSel.setAttribute('aria-label', t('time_range_label')); } catch { }
  try { if (sortModeSel2) sortModeSel2.setAttribute('aria-label', t('sort_label')); } catch { }
  try { if (timeRangeSel2) timeRangeSel2.setAttribute('aria-label', t('time_range_label')); } catch { }
  try { if (fcChip) fcChip.setAttribute('aria-label', t('fc_chip_label')); } catch { }
  try {
    [sortModeSel, sortModeSel2].filter(Boolean).forEach((sel) => {
      Array.from(sel.options || []).forEach((opt) => {
        const v = String(opt.value || '');
        if (v === 'new') opt.textContent = t('sort_new');
        if (v === 'monthly') opt.textContent = t('sort_monthly');
      });
    });
  } catch { }
  try {
    const fcLabel = document.querySelector('#fcPanel .fc-label');
    if (fcLabel) fcLabel.textContent = t('jump_label');
  } catch { }
  try { if (fcInput) fcInput.placeholder = t('jump_placeholder'); } catch { }
  try { if (fcGo) fcGo.textContent = t('btn_go'); } catch { }
	  try {
	    const fcSwitchText = document.querySelector('#fcPanel label[for="openWorkNewWindowToggle"] .fc-switch-text');
	    if (fcSwitchText) fcSwitchText.textContent = t('open_work_new_window');
	  } catch { }
	  try {
	    const el = document.querySelector('#fcPanel label[for="showSuspectInvalidTagToggle"] .fc-switch-text');
	    if (el) el.textContent = t('show_suspect_invalid_tags');
	  } catch { }
	  try {
	    const el = document.querySelector('#fcPanel label[for="showNaixInvalidTagToggle"] .fc-switch-text');
	    if (el) el.textContent = t('show_naix_invalid_tags');
	  } catch { }
  try { const fcQ = document.getElementById('fcQ'); if (fcQ) fcQ.placeholder = t('fc_q_placeholder'); } catch { }
  try { const fcPrompt = document.getElementById('fcPrompt'); if (fcPrompt) fcPrompt.placeholder = t('fc_prompt_placeholder'); } catch { }
  try { const fcBlacklist = document.getElementById('fcBlacklist'); if (fcBlacklist) fcBlacklist.placeholder = t('fc_blacklist_placeholder'); } catch { }
  try { const fcSearchBtn = document.getElementById('fcSearchBtn'); if (fcSearchBtn) fcSearchBtn.textContent = t('btn_search'); } catch { }
  try { const fcSaveBlacklistBtn = document.getElementById('fcSaveBlacklistBtn'); if (fcSaveBlacklistBtn) fcSaveBlacklistBtn.textContent = t('btn_save_blacklist'); } catch { }
  try { if (hpImg) hpImg.alt = t('preview_alt'); } catch { }
  try { if (backBtn) backBtn.textContent = t('back_btn'); } catch { }
  try { if (detailTitle) detailTitle.textContent = t('detail_header'); } catch { }
  try {
    const titleEl = document.getElementById('announceTitle');
    if (titleEl) titleEl.textContent = t('announce_title');
  } catch { }
  try { if (announceClose) announceClose.textContent = t('announce_close'); } catch { }
  try {
    const content = document.querySelector('#announceOverlay .announce-content');
    if (content) {
      const href = 'https://www.pixiv.net/messages.php?receiver_id=120618272';
      const linkHtml = `<a href="${href}" target="_blank" rel="noopener noreferrer">${escapeHtml(t('announce_strong_link'))}</a>`;
      const prefix = escapeHtml(t('announce_strong_prefix'));
      const suffix = escapeHtml(t('announce_strong_suffix'));
      content.innerHTML = `
        <p>${escapeHtml(t('announce_p1'))}</p>
        <p>${escapeHtml(t('announce_p2'))}</p>
        <p>${escapeHtml(t('announce_p3'))}</p>
        <p>${escapeHtml(t('announce_p4'))}</p>
        <p class="announce-strong">${prefix}${CURRENT_LANG === 'zh' ? '' : ' '}${linkHtml}${suffix ? (' ' + suffix) : ''}</p>
      `;
    }
  } catch { }
}

function setOrCreateMetaByName(name, content) {
  if (!name) return;
  const head = document.head || document.getElementsByTagName('head')[0];
  if (!head) return;
  let el = head.querySelector(`meta[name="${name}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute('name', name);
    head.appendChild(el);
  }
  el.setAttribute('content', String(content ?? ''));
}

function setOrCreateMetaByProperty(property, content) {
  if (!property) return;
  const head = document.head || document.getElementsByTagName('head')[0];
  if (!head) return;
  let el = head.querySelector(`meta[property="${property}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute('property', property);
    head.appendChild(el);
  }
  el.setAttribute('content', String(content ?? ''));
}

function setOrCreateLinkRel(rel, href) {
  if (!rel) return;
  const head = document.head || document.getElementsByTagName('head')[0];
  if (!head) return;
  let el = head.querySelector(`link[rel="${rel}"]`);
  if (!el) {
    el = document.createElement('link');
    el.setAttribute('rel', rel);
    head.appendChild(el);
  }
  el.setAttribute('href', String(href ?? ''));
}

function clearDynamicOgImages() {
  try {
    document.querySelectorAll('meta[property="og:image"][data-dynamic="1"]').forEach((n) => n.remove());
  } catch { }
  try {
    const tw = document.querySelector('meta[name="twitter:image"][data-dynamic="1"]');
    if (tw) tw.remove();
  } catch { }
}

function setDynamicOgImages(urls) {
  const head = document.head || document.getElementsByTagName('head')[0];
  if (!head) return;
  clearDynamicOgImages();
  const list = Array.isArray(urls) ? urls.filter(Boolean).slice(0, 8) : [];
  list.forEach((u) => {
    const m = document.createElement('meta');
    m.setAttribute('property', 'og:image');
    m.setAttribute('content', String(u));
    m.dataset.dynamic = '1';
    head.appendChild(m);
  });
  if (list.length) {
    const tw = document.createElement('meta');
    tw.setAttribute('name', 'twitter:image');
    tw.setAttribute('content', String(list[0]));
    tw.dataset.dynamic = '1';
    head.appendChild(tw);
  }
}

function compactOneLine(s) {
  return String(s ?? '').replace(/\s+/g, ' ').trim();
}

function applyHomeSeo() {
  const siteTitle = CURRENT_LANG === 'zh' ? SITE_TITLE_ZH : SITE_TITLE_EN;
  document.title = siteTitle;
  setOrCreateMetaByName('description', CURRENT_LANG === 'zh' ? HOME_DESC_ZH : HOME_DESC_EN);
  setOrCreateMetaByName('robots', 'index,follow,max-image-preview:large');
  setOrCreateMetaByProperty('og:title', siteTitle);
  setOrCreateMetaByProperty('og:description', CURRENT_LANG === 'zh' ? HOME_DESC_ZH : HOME_DESC_EN);
  setOrCreateMetaByProperty('og:type', 'website');
  setOrCreateMetaByProperty('og:site_name', siteTitle);
  setOrCreateMetaByProperty('og:locale', CURRENT_LANG === 'zh' ? 'zh_CN' : 'en_US');
  setOrCreateMetaByName('twitter:card', 'summary_large_image');
  setOrCreateMetaByName('twitter:title', siteTitle);
  setOrCreateMetaByName('twitter:description', CURRENT_LANG === 'zh' ? HOME_DESC_ZH : HOME_DESC_EN);
  const href = String(window.location.origin || '') + '/';
  setOrCreateMetaByProperty('og:url', href);
  setOrCreateLinkRel('canonical', href);
  clearDynamicOgImages();
}

function applyWorkSeo(workId, work = {}, images = []) {
  let typeRaw = String(work.AI_type || work.ai_type || '').trim();
  if (!typeRaw) {
    try {
      const first = Array.isArray(images) ? images[0] : null;
      if (first && first.image_type) typeRaw = String(first.image_type).trim();
    } catch { }
  }
  const typeLabel = typeRaw ? typeRaw.toUpperCase() : 'AI';
  const titleRaw = (work.title && String(work.title).trim()) ? String(work.title).trim() : '';
  const siteTitle = CURRENT_LANG === 'zh' ? SITE_TITLE_ZH : SITE_TITLE_EN;
  const workTitle = `[${typeLabel}] ${titleRaw || t('work_fallback', { id: workId })} - ${siteTitle}`;

  const tags = normalizeTags(work.tags);
  let aiJson = '';
  try {
    const first = Array.isArray(images) ? images[0] : null;
    if (first && first.ai_json != null) {
      if (typeof first.ai_json === 'string') {
        aiJson = first.ai_json;
      } else {
        aiJson = JSON.stringify(first.ai_json);
      }
    }
  } catch { }
  let desc = '';
  if (tags.length) desc += `${t('seo_tags_prefix')}: ${tags.slice(0, 80).join(', ')} `;
  if (aiJson) desc += `${t('seo_ai_meta_prefix')}: ${aiJson}`;
  desc = compactOneLine(desc).slice(0, 1200);

  document.title = workTitle;
  setOrCreateMetaByName('description', desc || (CURRENT_LANG === 'zh' ? HOME_DESC_ZH : HOME_DESC_EN));
  setOrCreateMetaByName('robots', 'index,follow,max-image-preview:large');
  setOrCreateMetaByProperty('og:title', workTitle);
  setOrCreateMetaByProperty('og:description', desc || (CURRENT_LANG === 'zh' ? HOME_DESC_ZH : HOME_DESC_EN));
  setOrCreateMetaByProperty('og:type', 'article');
  setOrCreateMetaByProperty('og:site_name', siteTitle);
  setOrCreateMetaByProperty('og:locale', CURRENT_LANG === 'zh' ? 'zh_CN' : 'en_US');
  setOrCreateMetaByName('twitter:card', 'summary_large_image');
  setOrCreateMetaByName('twitter:title', workTitle);
  setOrCreateMetaByName('twitter:description', desc || (CURRENT_LANG === 'zh' ? HOME_DESC_ZH : HOME_DESC_EN));
  const href = `${window.location.origin}/i/${workId}`;
  setOrCreateMetaByProperty('og:url', href);
  setOrCreateLinkRel('canonical', href);
  try {
    const urls = (Array.isArray(images) ? images : []).map((img) => buildImageUrl(img)).filter(Boolean);
    setDynamicOgImages(urls);
  } catch {
    clearDynamicOgImages();
  }
}

const state = {
  page: 1,
  pageSize: 60,
  q: '',
  prompt: '',
  blacklist: [],
  items: [],
  total: 0,
  preview: { index: 0, images: [], title: '', active: false, side: 'right', top: 16, anchorEl: null },
  cache: { works: new Map() },
  directDetail: false,
	  listMode: 'infinite',
	  openWorkInNewWindow: false,
	  showSuspectInvalidTags: false,
	  showNaixInvalidTags: false,
	  lang: CURRENT_LANG,
		  ads: { lastKey: '', preloaded: new Set(), preloadTimer: 0 },
		  workFlags: new Map(),
		  workPages: new Map(),
		  detailScroll: { currentWorkId: null, byWork: new Map(), restoreTimers: [], isRestoring: false },
		};
// 统一移动端断点与设备特性检测（移动端不启用悬浮预览）
const MOBILE_MAX_WIDTH = 800;
function supportsHover() {
  try { return window.matchMedia('(hover: hover) and (pointer: fine)').matches; } catch { return false; }
}
function shouldEnableHoverPreview() {
  return supportsHover() && window.innerWidth > MOBILE_MAX_WIDTH;
}

const galleryEl = document.getElementById('gallery');
const loadingEl = document.getElementById('loading');
const paginationEl = document.getElementById('pagination');
const loadMoreBtn = document.getElementById('loadMoreBtn');
const qInput = document.getElementById('q');
const promptInput = document.getElementById('prompt');
const searchBtn = document.getElementById('searchBtn');
const searchStatusEl = document.getElementById('searchStatus');
const noResultEl = document.getElementById('noResult');
const sortModeSel = document.getElementById('sortMode');
const timeRangeSel = document.getElementById('timeRange');
const sortModeSel2 = document.getElementById('sortMode2');
const timeRangeSel2 = document.getElementById('timeRange2');
const blacklistInput = document.getElementById('blacklist');
const saveBlacklistBtn = document.getElementById('saveBlacklistBtn');
let importOldBlacklistBtn = null;
// 右下角浮动控件元素（设置形状芯片）
const fcChip = document.getElementById('fcChip');
const fcNum = document.getElementById('fcNum');
const fcPanel = document.getElementById('fcPanel');
	const fcInput = document.getElementById('fcInput');
	const fcGo = document.getElementById('fcGo');
	const openWorkNewWindowToggle = document.getElementById('openWorkNewWindowToggle');
	const showSuspectInvalidTagToggle = document.getElementById('showSuspectInvalidTagToggle');
	const showNaixInvalidTagToggle = document.getElementById('showNaixInvalidTagToggle');

// 悬浮预览元素
const hoverPreview = document.getElementById('hoverPreview');
const hpImg = document.getElementById('hpImage');
const hpTitle = document.getElementById('hpTitle');
const hpCount = document.getElementById('hpCount');

const detailView = document.getElementById('detailView');
const backBtn = document.getElementById('backBtn');
const detailMeta = document.getElementById('detailMeta');
const detailImages = document.getElementById('detailImages');
const detailTitle = document.getElementById('detailTitle');

const announceOverlay = document.getElementById('announceOverlay');
const announceClose = document.getElementById('announceClose');

// 工具函数
const escapeHtml = (s = '') => String(s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
// 以对象字段拼接图片完整链接：asset_base_url + image_type/author_id/file_name.webp
function buildImageUrl(imgOrPath = '') {
  const baseRaw = String(CONFIG.asset_base_url || '').trim();
  const base = baseRaw.endsWith('/') ? baseRaw : (baseRaw + '/');
  // 首选：对象字段 image_type/author_id/file_name
  if (imgOrPath && typeof imgOrPath === 'object') {
    const t = String(imgOrPath.image_type || '').trim();
    const a = String(imgOrPath.author_id ?? '').trim();
    const f = String(imgOrPath.file_name || '').trim();
    if (t && a && f) {
      return `${base}${t}/${a}/${f}.webp`;
    }
  }
  // 兼容旧字符串 image_path 的回退：去前缀并修正扩展名
  let p = String(imgOrPath || '');
  p = p.replace(/^\/?www\/pixiv_ai_tag\//, '');
  p = p.replace(/^\/?pixiv_ai_tag\//, '');
  p = p.replace(/\.png$/i, '.webp');
  p = p.replace(/^\/+/, '');
  return base ? (base + p) : p;
}

function formatMetric(value) {
  const v = Number(value) || 0;
  if (v >= 1000000) return `${(v / 1000000).toFixed(1).replace(/\.0$/, '')}m`;
  if (v >= 10000) return `${(v / 10000).toFixed(1).replace(/\.0$/, '')}w`;
  if (v >= 1000) return `${(v / 1000).toFixed(1).replace(/\.0$/, '')}k`;
  return String(v);
}

function adsEnabled() {
  return !!(CONFIG.ads_enabled && Array.isArray(CONFIG.ads) && CONFIG.ads.length);
}

function currentAdDevice() {
  return window.innerWidth <= MOBILE_MAX_WIDTH ? 'mobile' : 'desktop';
}

function getAdVariants(placement = 'search') {
  if (!adsEnabled()) return [];
  const device = currentAdDevice();
  const fallbackDevice = device === 'mobile' ? 'desktop' : 'mobile';
  const targetLocation = placement === 'detail' ? 'detail' : 'search';
  const variants = [];
  CONFIG.ads.forEach((group) => {
    if (!group || typeof group !== 'object') return;
    const locations = Array.isArray(group.locations) && group.locations.length ? group.locations : ['all'];
    if (!(locations.includes('all') || locations.includes(targetLocation))) return;
    const groupId = String(group.id || group.name || 'media').trim();
    const name = String(group.name || groupId).trim() || groupId;
    const href = String(group.href || '').trim();
    if (!href) return;
    const deviceConfig = group[device] || group[fallbackDevice] || {};
    const images = Array.isArray(deviceConfig.images) ? deviceConfig.images : [];
    images.forEach((image, index) => {
      if (!image || typeof image !== 'object') return;
      const src = String(image.src || '').trim();
      if (!src) return;
      const width = Number(image.width || 0) > 0 ? Number(image.width) : 0;
      const height = Number(image.height || 0) > 0 ? Number(image.height) : 0;
      variants.push({
        key: `${device}:${groupId}:${src}:${index}`,
        groupId,
        name,
        href,
        src,
        width,
        height,
      });
    });
  });
  return variants;
}

function chooseAdVariant(placement = 'search') {
  const variants = getAdVariants(placement);
  if (!variants.length) return null;
  const device = currentAdDevice();
  const keyName = `gallery_ad_last_v1_${placement}_${device}`;
  let lastKey = state.ads.lastKey || '';
  try { lastKey = lastKey || localStorage.getItem(keyName) || ''; } catch { }
  let pool = variants.filter((v) => v.key !== lastKey);
  if (!pool.length) pool = variants;
  const picked = pool[Math.floor(Math.random() * pool.length)] || pool[0] || null;
  if (picked) {
    state.ads.lastKey = picked.key;
    try { localStorage.setItem(keyName, picked.key); } catch { }
  }
  return picked;
}

function shouldPreloadAdsOnSearchPage() {
  try {
    if (state.directDetail) return false;
    if (String(window.location.pathname || '').startsWith('/i/')) return false;
  } catch { }
  return true;
}

function getAdPreloadUrlsForCurrentPage() {
  if (!adsEnabled()) return [];
  const map = new Map();
  try {
    [...getAdVariants('search'), ...getAdVariants('detail')].forEach((ad) => {
      const src = String((ad && ad.src) || '').trim();
      if (src && !map.has(src)) map.set(src, src);
    });
  } catch { }
  return Array.from(map.values());
}

function scheduleSearchAdPreload() {
  if (!shouldPreloadAdsOnSearchPage()) return;
  const urls = getAdPreloadUrlsForCurrentPage().filter((src) => {
    try { return !state.ads.preloaded.has(src); } catch { return true; }
  });
  if (!urls.length) return;
  if (state.ads.preloadTimer) return;

  const run = () => {
    state.ads.preloadTimer = 0;
    urls.forEach((src, index) => {
      setTimeout(() => {
        try {
          if (state.ads.preloaded.has(src)) return;
          state.ads.preloaded.add(src);
          const img = new Image();
          img.decoding = 'async';
          try { img.fetchPriority = 'low'; } catch { }
          img.src = src;
        } catch { }
      }, index * 140);
    });
  };

  state.ads.preloadTimer = setTimeout(run, 120);
}

function createAdElement(placement = 'list') {
  const ad = chooseAdVariant(placement === 'detail' ? 'detail' : 'search');
  if (!ad) return null;
  const slot = document.createElement('div');
  slot.className = placement === 'detail' ? 'media-insert detail-insert' : 'media-insert gallery-insert';
  slot.dataset.insertGroup = ad.groupId;

  const link = document.createElement('a');
  link.className = 'media-insert-link';
  link.href = ad.href;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.title = ad.name;

  const img = document.createElement('img');
  img.className = 'media-insert-image';
  img.loading = 'eager';
  img.fetchPriority = 'high';
  img.decoding = 'async';
  img.alt = ad.name;
  img.src = ad.src;
  if (ad.width) {
    img.style.width = `${ad.width}px`;
  }
  if (ad.width && ad.height) {
    img.style.aspectRatio = `${ad.width} / ${ad.height}`;
  }
  link.appendChild(img);
  slot.appendChild(link);
  return slot;
}

function getGalleryColumnCount() {
  try {
    const cols = getComputedStyle(galleryEl).gridTemplateColumns;
    const count = String(cols || '').split(' ').filter(Boolean).length;
    if (count > 0) return count;
  } catch { }
  return window.innerWidth <= MOBILE_MAX_WIDTH ? 2 : 6;
}

function appendGalleryAd(slotKey) {
  if (!adsEnabled() || !galleryEl || !slotKey) return;
  if (galleryEl.querySelector(`[data-insert-slot="${slotKey}"]`)) return;
  const adEl = createAdElement('list');
  if (!adEl) return;
  adEl.dataset.insertSlot = slotKey;
  galleryEl.appendChild(adEl);
}

function getWorkListPage(w = {}) {
  try {
    const key = normalizeWorkId(w.id);
    const page = Number(state.workPages.get(key) || 0);
    if (Number.isFinite(page) && page >= 1) return page;
  } catch { }
  const fallback = Number(state.page || 1);
  return Number.isFinite(fallback) && fallback >= 1 ? fallback : 1;
}

function rememberWorkListPages(items = [], page = 1, opts = {}) {
  try {
    if (opts.reset) state.workPages.clear();
    const p = Math.max(1, Number(page) || 1);
    (Array.isArray(items) ? items : []).forEach((w) => {
      if (!w || w.id == null) return;
      const key = normalizeWorkId(w.id);
      if (!state.workPages.has(key)) state.workPages.set(key, p);
    });
  } catch { }
}

function isMonthlyMode() {
  const mode = (sortModeSel && sortModeSel.value) || (sortModeSel2 && sortModeSel2.value) || 'new';
  return mode === 'monthly';
}

// 提取文件中的页码（_pN），用于排序
function getPageIndex(obj) {
  const s = String((obj && (obj.file_name || obj.image_path)) || '');
  const m = s.match(/_p(\d+)/);
  return m ? parseInt(m[1], 10) : 0;
}
const snippet = (s = '', n = 80) => {
  const t = String(s).trim();
  return t.length > n ? t.slice(0, n) + '…' : t;
};
const typeClass = (t = '') => {
  const k = String(t).toLowerCase();
  if (k === 'sd') return 'sd';
  if (k === 'nai') return 'nai';
  if (k === 'nai_x' || k === 'naix' || k === 'nai x') return 'nai-x';
  if (k === 'comfyui') return 'comfyui';
  return '';
};
function normalizeWorkId(id) {
  const n = Number(id);
  return Number.isFinite(n) ? n : String(id || '');
}
function isNaixWork(w = {}) {
  const raw = String((w && (w.AI_type || w.ai_type || w.image_type)) || '').trim().toLowerCase();
  return raw === 'nai_x' || raw === 'naix' || raw === 'nai x';
}
function getWorkFlags(id) {
  return state.workFlags.get(normalizeWorkId(id)) || {};
}
function setWorkFlags(id, patch = {}) {
  const key = normalizeWorkId(id);
  const prev = state.workFlags.get(key) || {};
  const next = { ...prev, ...patch };
  state.workFlags.set(key, next);
  return next;
}
function isSuspectInvalidTagWorkData(workData) {
  try {
    const wtype = String((workData && (workData.work || {}).AI_type) || '').toLowerCase();
    if (wtype !== 'nai' && wtype !== 'nai_x') return false;
    return !!(window.NAIX && typeof window.NAIX.suspectWork === 'function' && window.NAIX.suspectWork(workData));
  } catch {
    return false;
  }
}
function rememberWorkFlagsFromDetail(workData) {
  const work = workData && workData.work ? workData.work : null;
  if (!work || work.id == null) return false;
  const key = normalizeWorkId(work.id);
  const prev = getWorkFlags(key);
  const nextSuspect = isSuspectInvalidTagWorkData(workData);
  const nextNaix = isNaixWork(work);
  if (prev.suspectInvalidTags === nextSuspect && prev.naixType === nextNaix) return false;
  setWorkFlags(key, { suspectInvalidTags: nextSuspect, naixType: nextNaix });
  return true;
}
function isFrontendHiddenWork(w = {}) {
  if (isBlockedWork(w)) return true;
  const flags = getWorkFlags(w.id);
  const isNaix = isNaixWork(w) || flags.naixType;
  const isSuspect = !!flags.suspectInvalidTags;
  if (isNaix || isSuspect) {
    const allowedByNaix = isNaix && state.showNaixInvalidTags;
    const allowedBySuspect = isSuspect && state.showSuspectInvalidTags;
    return !(allowedByNaix || allowedBySuspect);
  }
  return false;
}
function visibleWorks(items = state.items) {
  return (Array.isArray(items) ? items : []).filter((w) => !isFrontendHiddenWork(w));
}
function updateNoResultVisibility() {
  try {
    if (noResultEl) noResultEl.classList.toggle('visible', visibleWorks().length === 0);
  } catch { }
}
function removeInfiniteSentinel() {
  if (infiniteObserver) {
    try { infiniteObserver.disconnect(); } catch { }
    infiniteObserver = null;
  }
  try {
    const sentinel = document.getElementById('infiniteSentinel');
    if (sentinel) sentinel.remove();
  } catch { }
}
function setupInfiniteScrollIfVisible() {
  if (visibleWorks().length > 0) {
    setupInfiniteScroll();
  } else {
    removeInfiniteSentinel();
  }
}
function preserveWindowScrollAfterRender(fn) {
  const y = window.scrollY || window.pageYOffset || 0;
  try {
    fn();
  } finally {
    const restore = () => {
      try {
        window.scrollTo({ top: y, behavior: 'auto' });
      } catch {
        try { window.scrollTo(0, y); } catch { }
      }
    };
    restore();
    try { requestAnimationFrame(restore); } catch { }
    setTimeout(restore, 80);
  }
}

function hasEchoCheckpointLoaderSimple(obj) {
  const target = 'ECHOCheckpointLoaderSimple';
  try {
    const stack = [obj];
    const seen = new WeakSet();
    let steps = 0;
    while (stack.length && steps < 8000) {
      const cur = stack.pop();
      steps += 1;
      if (cur == null) continue;
      const t = typeof cur;
      if (t === 'string') {
        if (cur.includes(target)) return true;
        continue;
      }
      if (t !== 'object') continue;
      if (seen.has(cur)) continue;
      seen.add(cur);
      if (cur.class_type === target || cur.class === target || cur.type === target) return true;
      if (Array.isArray(cur)) {
        for (const v of cur) stack.push(v);
      } else {
        for (const v of Object.values(cur)) stack.push(v);
      }
    }
  } catch { }
  return false;
}

function isNonStandardComfyuiWork(workData) {
  try {
    const wtype = String((workData && (workData.work || {}).AI_type) || '').toLowerCase();
    if (wtype !== 'comfyui') return false;
    for (const img of (workData.images || [])) {
      const raw = img ? img.ai_json : null;
      if (!raw) continue;
      if (typeof raw === 'string') {
        if (raw.includes('ECHOCheckpointLoaderSimple')) return true;
        try {
          const obj = JSON.parse(raw);
          if (hasEchoCheckpointLoaderSimple(obj)) return true;
        } catch { }
      } else {
        if (hasEchoCheckpointLoaderSimple(raw)) return true;
      }
    }
  } catch { }
  return false;
}
// 将 ISO8601 字符串格式化为 "YYYY-MM-DD HH:MM:SS"（保留源字符串的日期与时分秒）
function formatDateTime(isoStr = '') {
  const s = String(isoStr || '').trim();
  const m = s.match(/^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})/);
  if (m) return `${m[1]} ${m[2]}`;
  // 兜底：若不符合预期，尝试 Date 解析后再拼接本地时间
  const d = new Date(s);
  if (!Number.isNaN(d.getTime())) {
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  }
  return s.replace('T', ' ').replace(/([+-]?\d{2}:?\d{2}|Z)$/, '');
}
// 仅格式化为日期（YYYY-MM-DD），用于首页卡片的投稿时间
function formatDate(isoStr = '') {
  const s = String(isoStr || '').trim();
  const m = s.match(/^(\d{4}-\d{2}-\d{2})/);
  if (m) return m[1];
  const d = new Date(s);
  if (!Number.isNaN(d.getTime())) {
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  }
  // 最后兜底：截取前 10 位（若是标准 ISO 字符串）
  return s.slice(0, 10);
}
// 渲染作品简介：保留安全的 <a> 与 <br>，其余标签去除并转义；兼容纯文本换行
function renderCaption(raw = '') {
  const s = String(raw || '');
  const container = document.createElement('div');
  container.innerHTML = s;
  const allowedSchemes = ['http:', 'https:'];
  function walk(node) {
    const ELEMENT_NODE = 1;
    const TEXT_NODE = 3;
    if (!node) return '';
    if (node.nodeType === TEXT_NODE) {
      const t = node.textContent || '';
      return escapeHtml(t).replace(/\r\n|\r|\n/g, '<br>');
    }
    if (node.nodeType !== ELEMENT_NODE) return '';
    const tag = String(node.tagName || '').toLowerCase();
    if (tag === 'br') return '<br>';
    if (tag === 'a') {
      let href = node.getAttribute('href') || '';
      try {
        const u = new URL(href, window.location.origin);
        if (allowedSchemes.includes(u.protocol)) href = u.href; else href = '';
      } catch { href = ''; }
      const inner = Array.from(node.childNodes).map(walk).join('');
      if (!href) return inner;
      return `<a href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">${inner || escapeHtml(href)}</a>`;
    }
    if (tag === 'p' || tag === 'div') {
      const inner = Array.from(node.childNodes).map(walk).join('');
      return /<br>\s*$/.test(inner) ? inner : inner + '<br>';
    }
    return Array.from(node.childNodes).map(walk).join('');
  }
  return Array.from(container.childNodes).map(walk).join('');
}
function normalizeTags(raw) {
  if (!raw) return [];
  try {
    const j = JSON.parse(raw);
    if (Array.isArray(j)) return j.map((x) => String(x)).filter(Boolean);
    if (typeof j === 'object' && j) return Object.values(j).map((x) => String(x)).filter(Boolean);
  } catch { }
  let buf = String(raw);
  for (const sep of ['\n', ',', '|', ';', ' ', '、', '，', '。', '\t']) buf = buf.split(sep).join(',');
  return buf.split(',').map((x) => x.trim()).filter(Boolean);
}

// 黑名单工具
function parseWords(s = '') {
  let buf = String(s);
  for (const sep of ['\n', ',', '|', ';', ' ', '、', '，', '。', '\t']) buf = buf.split(sep).join(',');
  return buf.split(',').map((x) => x.trim()).filter(Boolean);
}
function loadBlacklist() {
  try {
    const raw = localStorage.getItem('gallery_blacklist') || '';
    state.blacklist = parseWords(raw).map((x) => x.toLowerCase());
    blacklistInput.value = raw;
  } catch { }
}
function saveBlacklist() {
  const raw = blacklistInput.value || '';
  localStorage.setItem('gallery_blacklist', raw);
  state.blacklist = parseWords(raw).map((x) => x.toLowerCase());
}

const BLACKLIST_MIGRATE_DONE_PREFIX = 'gallery_blacklist_migrate_done_v2:';
function importBlacklistFromWindowNameIfNeeded() {
  try {
    const marker = 'gallery_migrate_bl_v1:';
    const name = String(window.name || '');
    if (!name.startsWith(marker)) return false;

    let encoded = name.slice(marker.length);
    let decoded = '';
    try { decoded = decodeURIComponent(encoded); } catch { decoded = ''; }
    try { window.name = ''; } catch { }

    if (!decoded.trim()) return false;
    let currentRaw = '';
    try { currentRaw = String(localStorage.getItem('gallery_blacklist') || ''); } catch { currentRaw = ''; }
    if (currentRaw.trim()) return false;

    try { localStorage.setItem('gallery_blacklist', decoded); } catch { }
    try { blacklistInput.value = decoded; } catch { }
    try { state.blacklist = parseWords(decoded).map((x) => x.toLowerCase()); } catch { }
    return true;
  } catch {
    try { window.name = ''; } catch { }
    return false;
  }
}
function importBlacklistFromHashIfNeeded() {
  try {
    let h = String(window.location.hash || '');
    if (!h) return false;
    if (!h.startsWith('#')) return false;
    const rawPart = h.slice(1);
    const parts = rawPart.split('&').filter(Boolean);
    if (!parts.length) return false;
    const kv = {};
    for (const p of parts) {
      const idx = p.indexOf('=');
      if (idx === -1) continue;
      const k = p.slice(0, idx);
      const v = p.slice(idx + 1);
      if (k) kv[k] = v;
    }
    if (!kv.migrate_bl) return false;

    let currentRaw = '';
    try { currentRaw = String(localStorage.getItem('gallery_blacklist') || ''); } catch { currentRaw = ''; }
    if (currentRaw.trim()) {
      const nextParts = parts.filter((p) => !p.startsWith('migrate_bl='));
      const nextHash = nextParts.length ? `#${nextParts.join('&')}` : '';
      history.replaceState(history.state || {}, '', window.location.pathname + window.location.search + nextHash);
      return false;
    }

    let decoded = '';
    try { decoded = decodeURIComponent(String(kv.migrate_bl || '')); } catch { decoded = ''; }
    if (!decoded.trim()) return false;
    try { localStorage.setItem('gallery_blacklist', decoded); } catch { }
    try { blacklistInput.value = decoded; } catch { }
    try { state.blacklist = parseWords(decoded).map((x) => x.toLowerCase()); } catch { }

    const nextParts = parts.filter((p) => !p.startsWith('migrate_bl='));
    const nextHash = nextParts.length ? `#${nextParts.join('&')}` : '';
    history.replaceState(history.state || {}, '', window.location.pathname + window.location.search + nextHash);
    return true;
  } catch {
    return false;
  }
}
function _normalizeOrigin(urlStr) {
  try {
    let s = String(urlStr || '').trim();
    if (!s) return '';
    if (!s.includes('://')) s = `https://${s}`;
    const u = new URL(s);
    return u.origin;
  } catch {
    return '';
  }
}

function oldBlacklistMigrationEnabled() {
  // 旧域名黑名单迁移功能保留，但默认由后端配置关闭。
  return !!CONFIG.old_blacklist_migrate_enabled;
}

function ensureImportOldBlacklistButton(oldOrigin) {
  if (!oldBlacklistMigrationEnabled()) return null;
  try {
    const host = document.getElementById('fcExtraSettings') || fcPanel;
    if (!host) return null;
    try {
      const existing = document.getElementById('importOldBlacklistBtn');
      if (existing && existing !== importOldBlacklistBtn) {
        try { existing.remove(); } catch { }
      }
    } catch { }
    if (importOldBlacklistBtn) {
      try {
        if (importOldBlacklistBtn.parentNode !== host) host.appendChild(importOldBlacklistBtn);
      } catch { }
      return importOldBlacklistBtn;
    }
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'importOldBlacklistBtn';
    btn.className = 'btn outline';
    btn.textContent = t('btn_import_blacklist');
    btn.addEventListener('click', async () => {
      try {
        const ok = await migrateBlacklistFromOldDomainViaPopup(oldOrigin);
        if (!importOldBlacklistBtn) return;
        if (ok) {
          importOldBlacklistBtn.textContent = t('import_blacklist_done');
          setTimeout(() => { try { if (importOldBlacklistBtn) importOldBlacklistBtn.remove(); } catch { } importOldBlacklistBtn = null; }, 900);
        } else {
          importOldBlacklistBtn.textContent = t('import_blacklist_failed');
          setTimeout(() => { try { if (importOldBlacklistBtn) importOldBlacklistBtn.textContent = t('btn_import_blacklist'); } catch { } }, 1600);
        }
      } catch { }
    });
    try {
      host.appendChild(btn);
    } catch {
      try { host.appendChild(btn); } catch { }
    }
    importOldBlacklistBtn = btn;
    return btn;
  } catch {
    return null;
  }
}

async function migrateBlacklistFromOldDomainViaPopup(oldOrigin) {
  if (!oldBlacklistMigrationEnabled()) return false;
  let currentRaw = '';
  try { currentRaw = String(localStorage.getItem('gallery_blacklist') || ''); } catch { currentRaw = ''; }
  if (currentRaw.trim()) return false;

  const btn = importOldBlacklistBtn;
  if (btn) {
    try { btn.disabled = true; } catch { }
    try { btn.textContent = t('import_blacklist_starting'); } catch { }
  }

  const targetOrigin = encodeURIComponent(window.location.origin);
  const url = `${oldOrigin}/api/migrate/blacklist?target_origin=${targetOrigin}`;
  const w = window.open(url, 'migrate_blacklist', 'popup=yes,width=520,height=520');
  if (!w) {
    if (btn) { try { btn.disabled = false; btn.textContent = t('btn_import_blacklist'); } catch { } }
    try { alert(t('import_blacklist_popup_blocked')); } catch { }
    return false;
  }

  return await new Promise((resolve) => {
    let settled = false;
    let timer = null;

    const cleanup = () => {
      try { window.removeEventListener('message', onMsg); } catch { }
      if (timer) { try { clearTimeout(timer); } catch { } timer = null; }
      try { if (w && !w.closed) w.close(); } catch { }
      if (btn) { try { btn.disabled = false; } catch { } }
    };
    const finalize = (ok) => {
      if (settled) return;
      settled = true;
      cleanup();
      resolve(!!ok);
    };
    const onMsg = (e) => {
      try {
        if (!e || e.origin !== oldOrigin) return;
        const data = e.data || {};
        if (!data || data.type !== 'gallery_blacklist_migrate_v1') return;
        if (!data.ok) return finalize(false);
        const raw = String(data.raw || '');
        if (!raw.trim()) return finalize(false);
        let currentNow = '';
        try { currentNow = String(localStorage.getItem('gallery_blacklist') || ''); } catch { currentNow = ''; }
        if (currentNow.trim()) return finalize(false);
        try { localStorage.setItem('gallery_blacklist', raw); } catch { }
        try { blacklistInput.value = raw; } catch { }
        try { state.blacklist = parseWords(raw).map((x) => x.toLowerCase()); } catch { }
        finalize(true);
      } catch {
        finalize(false);
      }
    };

    try { window.addEventListener('message', onMsg); } catch { }
    timer = setTimeout(() => finalize(false), 15000);
  });
}

async function migrateBlacklistFromOldDomainIfNeeded() {
  if (!oldBlacklistMigrationEnabled()) return false;
  let currentRaw = '';
  try { currentRaw = String(localStorage.getItem('gallery_blacklist') || ''); } catch { currentRaw = ''; }
  if (currentRaw.trim()) return false;

  const oldOrigin = _normalizeOrigin(CONFIG.old_domain || '');
  if (!oldOrigin) return false;
  if (oldOrigin === window.location.origin) return false;

  const doneKey = `${BLACKLIST_MIGRATE_DONE_PREFIX}${oldOrigin}`;
  try { if (localStorage.getItem(doneKey) === '1') return false; } catch { }

  const okIframe = await new Promise((resolve) => {
    let settled = false;
    let iframe = null;
    let timer = null;

    const cleanup = () => {
      try { window.removeEventListener('message', onMsg); } catch { }
      if (timer) { try { clearTimeout(timer); } catch { } timer = null; }
      if (iframe) { try { iframe.remove(); } catch { } iframe = null; }
    };
    const finalize = (ok) => {
      if (settled) return;
      settled = true;
      if (ok) {
        try { localStorage.setItem(doneKey, '1'); } catch { }
      }
      cleanup();
      resolve(!!ok);
    };
    const onMsg = (e) => {
      try {
        if (!e || e.origin !== oldOrigin) return;
        const data = e.data || {};
        if (!data || data.type !== 'gallery_blacklist_migrate_v1') return;
        if (!data.ok) return finalize(false);
        const raw = String(data.raw || '');
        if (!raw.trim()) return finalize(false);
        let currentNow = '';
        try { currentNow = String(localStorage.getItem('gallery_blacklist') || ''); } catch { currentNow = ''; }
        if (currentNow.trim()) return finalize(false);
        try { localStorage.setItem('gallery_blacklist', raw); } catch { }
        try { blacklistInput.value = raw; } catch { }
        try { state.blacklist = parseWords(raw).map((x) => x.toLowerCase()); } catch { }
        finalize(true);
      } catch {
        finalize(false);
      }
    };

    try { window.addEventListener('message', onMsg); } catch { }
    timer = setTimeout(() => finalize(false), 2500);
    try {
      iframe = document.createElement('iframe');
      iframe.style.position = 'fixed';
      iframe.style.left = '-9999px';
      iframe.style.top = '-9999px';
      iframe.style.width = '1px';
      iframe.style.height = '1px';
      iframe.style.opacity = '0';
      iframe.style.pointerEvents = 'none';
      const targetOrigin = encodeURIComponent(window.location.origin);
      iframe.src = `${oldOrigin}/api/migrate/blacklist?target_origin=${targetOrigin}`;
      document.body.appendChild(iframe);
    } catch {
      finalize(false);
    }
  });
  if (!okIframe) {
    try { ensureImportOldBlacklistButton(oldOrigin); } catch { }
  } else {
    try { if (importOldBlacklistBtn) { importOldBlacklistBtn.remove(); importOldBlacklistBtn = null; } } catch { }
  }
  return okIframe;
}

function migrateBlacklistFromOldDomainInBackground() {
  if (!oldBlacklistMigrationEnabled()) return;
  try {
    migrateBlacklistFromOldDomainIfNeeded().then((ok) => {
      if (!ok) return;
      // 旧域名黑名单迁移成功后，只刷新前端过滤结果，不阻塞初始作品加载。
      try { refreshCurrentGallery({ preserveScroll: true }); } catch { }
    }).catch(() => { });
  } catch { }
}

		const OPEN_WORK_NEW_WINDOW_KEY = 'open_work_new_window_v1';
	const SHOW_SUSPECT_INVALID_TAGS_KEY = 'gallery_show_suspect_invalid_tags_v1';
	const SHOW_NAIX_INVALID_TAGS_KEY = 'gallery_show_naix_invalid_tags_v1';
		const CONFIG_REQUEST_VERSION = '260528a';
	const CONFIG_CACHE_JSON_KEY = 'gallery_config_json_v6';
	const CONFIG_CACHE_TS_KEY = 'gallery_config_ts_v6';
function loadOpenWorkInNewWindow() {
  let v = false;
  try { v = localStorage.getItem(OPEN_WORK_NEW_WINDOW_KEY) === '1'; } catch { }
  state.openWorkInNewWindow = v;
  try { if (openWorkNewWindowToggle) openWorkNewWindowToggle.checked = v; } catch { }
}
	function setOpenWorkInNewWindow(v) {
	  state.openWorkInNewWindow = !!v;
	  try { localStorage.setItem(OPEN_WORK_NEW_WINDOW_KEY, state.openWorkInNewWindow ? '1' : '0'); } catch { }
	  try { if (openWorkNewWindowToggle) openWorkNewWindowToggle.checked = state.openWorkInNewWindow; } catch { }
	}
	function syncInvalidTagToggles() {
	  try { if (showSuspectInvalidTagToggle) showSuspectInvalidTagToggle.checked = !!state.showSuspectInvalidTags; } catch { }
	  try { if (showNaixInvalidTagToggle) showNaixInvalidTagToggle.checked = !!state.showNaixInvalidTags; } catch { }
	}
	function loadInvalidTagFilterSettings() {
	  let showSuspect = false;
	  let showNaix = false;
	  try { showSuspect = localStorage.getItem(SHOW_SUSPECT_INVALID_TAGS_KEY) === '1'; } catch { }
	  try { showNaix = localStorage.getItem(SHOW_NAIX_INVALID_TAGS_KEY) === '1'; } catch { }
	  state.showSuspectInvalidTags = showSuspect;
	  state.showNaixInvalidTags = showNaix;
	  syncInvalidTagToggles();
	}
function refreshCurrentGallery(opts = {}) {
  const work = () => {
    try { closePreview(); } catch { }
    renderGallery({ forceClear: true });
    updateNoResultVisibility();
    if (state.listMode === 'pagination') {
      try { renderPagination(); } catch { }
    } else {
      try { setupInfiniteScrollIfVisible(); } catch { }
    }
  };
  if (opts.preserveScroll) {
    preserveWindowScrollAfterRender(work);
  } else {
    work();
  }
}
	let frontendFilterRefreshTimer = null;
	function scheduleFrontendFilterRefresh() {
	  if (frontendFilterRefreshTimer) return;
		  frontendFilterRefreshTimer = setTimeout(() => {
		    frontendFilterRefreshTimer = null;
		    refreshCurrentGallery({ preserveScroll: true });
		  }, 0);
		}
	function setShowSuspectInvalidTags(v) {
		  state.showSuspectInvalidTags = !!v;
		  try { localStorage.setItem(SHOW_SUSPECT_INVALID_TAGS_KEY, state.showSuspectInvalidTags ? '1' : '0'); } catch { }
		  syncInvalidTagToggles();
		  refreshCurrentGallery({ preserveScroll: true });
		}
	function setShowNaixInvalidTags(v) {
		  state.showNaixInvalidTags = !!v;
		  try { localStorage.setItem(SHOW_NAIX_INVALID_TAGS_KEY, state.showNaixInvalidTags ? '1' : '0'); } catch { }
		  syncInvalidTagToggles();
		  refreshCurrentGallery({ preserveScroll: true });
		}

async function getConfig() {
  try {
    const now = Date.now();
    const TTL_MS = 60 * 1000;
    const cachedStr = localStorage.getItem(CONFIG_CACHE_JSON_KEY) || '';
    const cachedTs = parseInt(localStorage.getItem(CONFIG_CACHE_TS_KEY) || '0', 10);
    if (cachedStr && cachedTs && (now - cachedTs) < TTL_MS) {
      try {
        const cached = JSON.parse(cachedStr);
        CONFIG = Object.assign(CONFIG, cached);
        // 从缓存配置填充首页公告。
        try {
          const annZh = String(cached.homepage_announcement_zh || '').trim();
          const annEn = String(cached.homepage_announcement_en || '').trim();
          const annEl = document.getElementById('heroAnnouncement');
          const annZhEl = document.getElementById('heroAnnouncementZh');
          const annEnEl = document.getElementById('heroAnnouncementEn');
          if (annEl && (annZh || annEn)) {
            if (annZhEl) annZhEl.textContent = annZh;
            if (annEnEl) annEnEl.textContent = annEn;
            annEl.classList.remove('hidden');
          }
        } catch { }
        return CONFIG;
      } catch { }
    }
    const res = await fetch(`${API_BASE}/api/config?v=${CONFIG_REQUEST_VERSION}`);
    const cfg = res.ok ? await res.json() : {};
    CONFIG = Object.assign(CONFIG, cfg);
    try {
      const years = Array.isArray(cfg.available_years) ? cfg.available_years : [];
      const months = Array.isArray(cfg.available_months) ? cfg.available_months : [];
      const tr = timeRangeSel;
      const tr2 = timeRangeSel2;
      if (tr) {
        // 清空并重建选项
        tr.innerHTML = '';
        const optAll = document.createElement('option'); optAll.value = 'all'; optAll.textContent = t('time_all'); tr.appendChild(optAll);
        // 年份（按年）；2023年不再细分季度，9月之前归入“更老”
        const yrs = years.length ? years : [2026, 2025, 2024, 2023];
        yrs.sort((a, b) => b - a);
        for (const y of yrs) {
          const optY = document.createElement('option'); optY.value = `y${y}`; optY.textContent = t('time_full_year', { year: y }); tr.appendChild(optY);
          if (y !== 2023) {
            for (let q = 1; q <= 4; q++) {
              const optQ = document.createElement('option'); optQ.value = `q${y}Q${q}`; optQ.textContent = t('time_quarter', { year: y, quarter: q }); tr.appendChild(optQ);
            }
          }
        }
        const optOlder = document.createElement('option'); optOlder.value = 'older'; optOlder.textContent = t('time_older'); tr.appendChild(optOlder);
      }
      if (tr && tr2) { tr2.innerHTML = tr.innerHTML; }
      const sm = sortModeSel;
      const sm2 = sortModeSel2;
      if (sm && tr) {
        sm.addEventListener('change', () => {
          const mode = sm.value || 'new';
          // 当切换到“每月排行榜”时，默认时间范围为“当前月份”；列表为“全部时间”
          if (mode === 'monthly') {
            const now = new Date(); const y = now.getFullYear(); const m = String(now.getMonth() + 1).padStart(2, '0');
            // 在排行榜模式下另采用 months 列表；若无 months 列表则构建 2025/2024 月份
            rebuildMonthlyOptions(months);
            tr.value = `m${y}-${m}`;
            if (tr2) tr2.value = tr.value;
            if (sm2) sm2.value = mode;
          } else {
            rebuildTimeOptions();
            tr.value = 'all';
            if (tr2) tr2.value = tr.value;
            if (sm2) sm2.value = mode;
          }
          triggerSearch();
        });
      }
      if (sm2 && tr2) {
        sm2.addEventListener('change', () => {
          const mode = sm2.value || 'new';
          if (sortModeSel) sortModeSel.value = mode;
          if (mode === 'monthly') {
            const now = new Date(); const y = now.getFullYear(); const m = String(now.getMonth() + 1).padStart(2, '0');
            rebuildMonthlyOptions(months);
            tr2.value = `m${y}-${m}`;
            if (timeRangeSel) timeRangeSel.value = tr2.value;
          } else {
            rebuildTimeOptions();
            tr2.value = 'all';
            if (timeRangeSel) timeRangeSel.value = tr2.value;
          }
          triggerSearch();
        });
      }
      if (tr) {
        tr.addEventListener('change', () => {
          triggerSearch();
        });
      }
      if (tr2) {
        tr2.addEventListener('change', () => {
          if (timeRangeSel) timeRangeSel.value = tr2.value;
          triggerSearch();
        });
      }
    } catch { }
    // 从后端配置填充首页公告。
    try {
      const annZh = String(cfg.homepage_announcement_zh || '').trim();
      const annEn = String(cfg.homepage_announcement_en || '').trim();
      const annEl = document.getElementById('heroAnnouncement');
      const annZhEl = document.getElementById('heroAnnouncementZh');
      const annEnEl = document.getElementById('heroAnnouncementEn');
      if (annEl && (annZh || annEn)) {
        if (annZhEl) annZhEl.textContent = annZh;
        if (annEnEl) annEnEl.textContent = annEn;
        annEl.classList.remove('hidden');
      }
    } catch { }
    try {
      localStorage.setItem(CONFIG_CACHE_JSON_KEY, JSON.stringify(cfg));
      localStorage.setItem(CONFIG_CACHE_TS_KEY, String(now));
    } catch { }
    return CONFIG;
  } catch {
    return CONFIG;
  }
}

function rebuildTimeOptions() {
  const tr = timeRangeSel; if (!tr) return;
  const yrs = Array.isArray(CONFIG.available_years) && CONFIG.available_years.length ? CONFIG.available_years.slice() : [2025, 2024, 2023];
  yrs.sort((a, b) => b - a);
  tr.innerHTML = '';
  for (const y of yrs) {
    const optY = document.createElement('option'); optY.value = `y${y}`; optY.textContent = t('time_full_year', { year: y }); tr.appendChild(optY);
    if (y > 2023) {
      for (let q = 1; q <= 4; q++) { const optQ = document.createElement('option'); optQ.value = `q${y}Q${q}`; optQ.textContent = t('time_quarter', { year: y, quarter: q }); tr.appendChild(optQ); }
    } else if (y === 2023) {
      const optQ4 = document.createElement('option'); optQ4.value = 'q2023Q4'; optQ4.textContent = t('time_quarter', { year: 2023, quarter: 4 }); tr.appendChild(optQ4);
    }
  }
  const optOlder = document.createElement('option'); optOlder.value = 'older'; optOlder.textContent = t('time_older'); tr.appendChild(optOlder);
  if (timeRangeSel2) timeRangeSel2.innerHTML = tr.innerHTML;
}

function rebuildMonthlyOptions(months) {
  const tr = timeRangeSel; if (!tr) return;
  tr.innerHTML = '';
  const optCur = document.createElement('option'); optCur.value = 'current'; optCur.textContent = t('time_current_month'); tr.appendChild(optCur);
  const yrs = Array.isArray(CONFIG.available_years) && CONFIG.available_years.length ? CONFIG.available_years.slice() : [2025, 2024, 2023];
  yrs.sort((a, b) => b - a);
  // 逐年月份
  const monthsList = Array.isArray(months) ? months.slice() : [];
  // 仅保留从 2023-11 及之后的月份
  const monthsFiltered = monthsList.filter((ym) => {
    try {
      const y = parseInt(String(ym).slice(0, 4), 10);
      const m = parseInt(String(ym).slice(5, 7), 10);
      if (y < 2023) return false;
      if (y === 2023 && m < 11) return false;
      return true;
    } catch { return false; }
  });
  const monthsByYear = new Map();
  for (const ym of monthsFiltered) {
    const y = parseInt(String(ym).slice(0, 4), 10);
    if (!monthsByYear.has(y)) monthsByYear.set(y, []);
    monthsByYear.get(y).push(String(ym));
  }
  for (const y of yrs) {
    const ms = monthsByYear.get(y) || [];
    ms.sort().reverse();
    for (const ym of ms) {
      const optM = document.createElement('option'); optM.value = `m${ym}`; optM.textContent = `${ym}`; tr.appendChild(optM);
    }
  }
  const optOlder = document.createElement('option'); optOlder.value = 'older'; optOlder.textContent = t('time_older'); tr.appendChild(optOlder);
  if (timeRangeSel2) timeRangeSel2.innerHTML = tr.innerHTML;
}

async function decodeBlacklistSet(blob) {
  try {
    if (CONFIG._blacklist_set && CONFIG.config_version) return CONFIG._blacklist_set;
    const c = _b64uToBytes(blob.c || '');
    const iv = _b64uToBytes(blob.iv || '');
    const s = _b64uToBytes(blob.s || '');
    if (!c.length || !iv.length) return new Set();
    const plain = new Uint8Array(c.length);
    let off = 0, idx = 0;
    if (window.crypto && crypto.subtle) {
      const keyRaw = s.length ? s : _utf8Bytes('AiGalleryMask_2025');
      const key = await crypto.subtle.importKey('raw', keyRaw, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
      while (off < c.length) {
        const counter = _concat(iv, _u32be(idx));
        const ksBuf = await crypto.subtle.sign('HMAC', key, counter);
        const ks = new Uint8Array(ksBuf);
        const len = Math.min(32, c.length - off);
        for (let j = 0; j < len; j++) plain[off + j] = c[off + j] ^ ks[j];
        off += len; idx += 1;
      }
    } else {
      while (off < c.length) {
        const counter = _concat(iv, _u32be(idx));
        const ks = _hmacSha256(s.length ? s : 'AiGalleryMask_2025', counter);
        const len = Math.min(32, c.length - off);
        for (let j = 0; j < len; j++) plain[off + j] = c[off + j] ^ ks[j];
        off += len; idx += 1;
      }
    }
    let listStr = '';
    try { listStr = new TextDecoder().decode(plain); } catch { listStr = _bytesToAscii(plain); }
    const ids = listStr.split(',').map((x) => parseInt(x, 10)).filter((n) => !Number.isNaN(n));
    const set = new Set(ids);
    CONFIG._blacklist_set = set;
    return set;
  } catch { return new Set(); }
}

function _utf8Bytes(s) {
  try { return new TextEncoder().encode(String(s)); } catch (e) { var u = unescape(encodeURIComponent(String(s))); var a = new Uint8Array(u.length); for (var i = 0; i < u.length; i++) { a[i] = u.charCodeAt(i); } return a; }
}
function _b64uToBytes(s) { s = String(s || '').replace(/-/g, '+').replace(/_/g, '/'); var pad = s.length % 4; if (pad) s += '='.repeat(4 - pad); var b = atob(s); var a = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) { a[i] = b.charCodeAt(i); } return a; }
function _bytesToAscii(u) { var s = ''; for (var i = 0; i < u.length; i++) { s += String.fromCharCode(u[i]); } return s; }
function _concat(a, b) { var out = new Uint8Array(a.length + b.length); out.set(a, 0); out.set(b, a.length); return out; }
function _u32be(n) { var a = new Uint8Array(4); a[0] = (n >>> 24) & 255; a[1] = (n >>> 16) & 255; a[2] = (n >>> 8) & 255; a[3] = n & 255; return a; }
function _sha256(msg) {
  var K = [1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555084734, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298];
  var H = [1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541445756];
  var i, j, t1, t2, a, b, c, d, e, f, g, h;
  var bytes = (msg instanceof Uint8Array) ? msg : _utf8Bytes(msg); var l = bytes.length; var withOne = new Uint8Array(l + 1); withOne.set(bytes, 0); withOne[l] = 0x80; var padLen = ((withOne.length + 8 + 64) >> 6 << 6); var buf = new Uint8Array(padLen); buf.set(withOne, 0); var bitLen = l * 8; buf[padLen - 4] = (bitLen >>> 24) & 255; buf[padLen - 3] = (bitLen >>> 16) & 255; buf[padLen - 2] = (bitLen >>> 8) & 255; buf[padLen - 1] = bitLen & 255;
  for (i = 0; i < buf.length; i += 64) {
    var w = new Uint32Array(64); for (j = 0; j < 16; j++) { var idx = i + j * 4; w[j] = (buf[idx] << 24) | (buf[idx + 1] << 16) | (buf[idx + 2] << 8) | (buf[idx + 3]); }
    for (j = 16; j < 64; j++) { var s0 = ((w[j - 15] >>> 7) | (w[j - 15] << 25)) ^ ((w[j - 15] >>> 18) | (w[j - 15] << 14)) ^ (w[j - 15] >>> 3); var s1 = ((w[j - 2] >>> 17) | (w[j - 2] << 15)) ^ ((w[j - 2] >>> 19) | (w[j - 2] << 13)) ^ (w[j - 2] >>> 10); w[j] = (w[j - 16] + s0 + w[j - 7] + s1) | 0; }
    a = H[0]; b = H[1]; c = H[2]; d = H[3]; e = H[4]; f = H[5]; g = H[6]; h = H[7];
    for (j = 0; j < 64; j++) { var S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7)); var ch = (e & f) ^ (~e & g); var temp1 = (h + S1 + ch + K[j] + w[j]) | 0; var S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10)); var maj = (a & b) ^ (a & c) ^ (b & c); var temp2 = (S0 + maj) | 0; h = g; g = f; f = e; e = (d + temp1) | 0; d = c; c = b; b = a; a = (temp1 + temp2) | 0; }
    H[0] = (H[0] + a) | 0; H[1] = (H[1] + b) | 0; H[2] = (H[2] + c) | 0; H[3] = (H[3] + d) | 0; H[4] = (H[4] + e) | 0; H[5] = (H[5] + f) | 0; H[6] = (H[6] + g) | 0; H[7] = (H[7] + h) | 0;
  }
  var out = new Uint8Array(32); for (i = 0; i < 8; i++) { out[i * 4] = (H[i] >>> 24) & 255; out[i * 4 + 1] = (H[i] >>> 16) & 255; out[i * 4 + 2] = (H[i] >>> 8) & 255; out[i * 4 + 3] = H[i] & 255; } return out;
}
function _hmacSha256(key, data) { var k = (key instanceof Uint8Array) ? key : _utf8Bytes(key); if (k.length > 64) k = _sha256(k); var kp = new Uint8Array(64); kp.set(k, 0); var ipad = new Uint8Array(64); var opad = new Uint8Array(64); for (var i = 0; i < 64; i++) { ipad[i] = kp[i] ^ 0x36; opad[i] = kp[i] ^ 0x5c; } var inner = _sha256(_concat(ipad, (data instanceof Uint8Array) ? data : _utf8Bytes(data))); return _sha256(_concat(opad, inner)); }
function isBlockedWork(w) {
  if (!state.blacklist.length) return false;
  const hay = [w.title, w.caption, w.tags, w.AI_type].map((v) => String(v || '').toLowerCase()).join('\n');
  return state.blacklist.some((kw) => kw && hay.includes(kw));
}

function syntaxHighlight(jsonStr) {
  // naive highlighter for JSON
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  let html = esc(jsonStr)
    .replace(/(".*?")(?=\s*:)/g, '<span class="k">$1</span>')
    .replace(/:\s*"(.*?)"/g, ':<span class="s">"$1"</span>')
    .replace(/:\s*(\d+(?:\.\d+)?)/g, ':<span class="n">$1</span>')
    .replace(/:\s*(true|false|null)/g, ':<span class="b">$1</span>');

  // Highlight common SD parameter prefixes within string content
  const sdPattern = /\b(Negative prompt|Steps|Sampler|Schedule type|CFG scale|Seed|Size|Model hash|Model|Denoising strength|Clip skip|Eta|Noise|Upscaler|Hires steps|Hires upscaler|Hires scale|Hires denoising strength|Mask blur|Inpaint area|Masked area padding|Lora hashes|Version|Style Selector Enabled|Style Selector Randomize|Style Selector Style|ADetailer confidence|ADetailer dilate erode|ADetailer mask blur|ADetailer inpaint only masked|ADetailer inpaint padding|ADetailer denoising strength|ADetailer model|ADetailer prompt)\s*:/gi;
  html = html.replace(sdPattern, (m) => `<span class="sd">${m}</span>`);

  // Highlight <lora:...> fragments and ensure the entire token is orange/bold
  // Previous JSON number highlighting may have inserted <span class="n"> inside the token;
  // we strip inner span tags within the matched lora segment so it becomes one colored block.
  html = html.replace(/(&lt;lora:)[\s\S]*?&gt;/gi, (m) => {
    const cleaned = m.replace(/<\/?span[^>]*>/g, '');
    return `<span class="sd-lora">${cleaned}</span>`;
  });

  return html;
}

// 详情页 JSON 框全局展开/折叠状态与注册表
let detailJsonBoxes = [];
let detailJsonExpanded = false;

// 无限滚动加载状态与终止标记
let loadingPage = false;
let endReached = false;
let lastPageCount = 0;

async function fetchWorks() {
  let keepSearchNotice = false;
  try {
    if (searchStatusEl) {
      searchStatusEl.classList.remove('notice');
      const textEl = searchStatusEl.querySelector('span');
      if (textEl) textEl.textContent = t('status_searching');
      searchStatusEl.classList.add('visible');
    }
  } catch { }
  loadingPage = true;
  loadingEl.textContent = t('loading');
  loadingEl.style.display = 'block';
  const mode = (sortModeSel && sortModeSel.value) || 'new';
  const isRank = mode === 'monthly';
  let url;
  if (isRank) {
    const trVal = (timeRangeSel && timeRangeSel.value) || 'current';
    if (trVal === 'current') {
      url = new URL('/api/rank/monthly/real', API_BASE);
    } else if (trVal === 'older' || (trVal.startsWith('m'))) {
      url = new URL('/api/rank/monthly/fixed', API_BASE);
    } else {
      url = new URL('/api/rank/monthly', API_BASE);
    }
  } else {
    url = new URL('/api/ai_works_search', API_BASE);
  }
  url.searchParams.set('page', state.page);
  url.searchParams.set('page_size', state.pageSize);
  if (state.q) url.searchParams.set('q', state.q);
  if (state.prompt) url.searchParams.set('prompt', state.prompt);
  const tr = (timeRangeSel && timeRangeSel.value) || (isRank ? 'current' : 'all');
  if (isRank) {
    // period 参数：current 或 YYYY-MM 或 older
    const path = url.pathname || '';
    if (path.includes('/real')) {
      // 当前月份不需要 period
    } else if (path.includes('/fixed')) {
      let month = '';
      if (tr === 'older') month = 'older';
      else if (tr && tr.startsWith('m')) month = tr.slice(1);
      url.searchParams.set('month', month);
    } else {
      let period = 'current';
      if (tr && tr.startsWith('m')) period = tr.slice(1);
      else if (tr === 'older') period = 'older';
      url.searchParams.set('period', period);
    }
    // 月榜也支持关键词与 prompt 过滤
    if (state.q) url.searchParams.set('q', state.q);
    if (state.prompt) url.searchParams.set('prompt', state.prompt);
  } else {
    // 列表接口：sort 与 time_range
    url.searchParams.set('sort', mode || 'new');
    url.searchParams.set('time_range', tr || 'all');
  }
  try {
    const res = await fetch(url);
    let data = {};
    try {
      data = await res.json();
    } catch { data = { page: state.page, page_size: state.pageSize, total: 0, items: [] }; }
    if (!res.ok && data && data.error === 'rank_processing') {
      const msg = CURRENT_LANG === 'zh'
        ? (data.message_zh || t('rank_processing'))
        : (data.message_en || t('rank_processing'));
	      state.items = [];
	      state.total = 0;
      try { state.workPages.clear(); } catch { }
	      lastPageCount = 0;
      renderGallery();
      if (paginationEl) paginationEl.innerHTML = '';
      if (loadMoreBtn) loadMoreBtn.classList.add('hidden');
      try { if (noResultEl) noResultEl.classList.remove('visible'); } catch { }
      try {
        if (searchStatusEl) {
          const textEl = searchStatusEl.querySelector('span');
          if (textEl) textEl.textContent = msg;
          searchStatusEl.classList.add('visible', 'notice');
          keepSearchNotice = true;
        }
      } catch { }
      return;
	    }
		    // 保留接口原始结果，具体隐藏规则统一在前端渲染时应用，方便开关即时恢复。
		    const incoming = Array.isArray(data.items) ? data.items : [];
		    lastPageCount = incoming.length;
    rememberWorkListPages(incoming, state.page, { reset: !(state.listMode === 'infinite' && state.page > 1) });
	    if (state.listMode === 'infinite' && state.page > 1) {
      // 追加并按 id 去重
      const prev = state.items || [];
      const map = new Map(prev.map((w) => [w.id, w]));
      for (const w of incoming) {
        if (!map.has(w.id)) map.set(w.id, w);
      }
      state.items = Array.from(map.values());
	    } else {
	      state.items = incoming;
	    }
	    state.total = data.total || 0;
	    renderGallery();
	    updateNoResultVisibility();
	    if (state.listMode === 'pagination') {
      renderPagination();
    }
	    if (state.listMode === 'infinite') {
	      setupInfiniteScrollIfVisible();
      // 根据是否还有下一页，切换“加载更多”按钮显示
      const totalPages = Math.max(1, Math.ceil((state.total || 0) / (state.pageSize || 1)));
      const unknownTotal = (state.total <= 0);
      endReached = unknownTotal ? (lastPageCount < state.pageSize) : (state.page >= totalPages);
      if (loadMoreBtn) {
        loadMoreBtn.classList.toggle('hidden', endReached);
      }
    }
  } catch (e) {
    loadingEl.textContent = t('loading_failed');
    try { if (noResultEl) noResultEl.classList.add('visible'); } catch { }
  } finally {
    loadingEl.style.display = 'none';
    loadingPage = false;
    try {
      if (searchStatusEl && !keepSearchNotice) {
        searchStatusEl.classList.remove('visible', 'notice');
      }
    } catch { }
  }
}

function renderGallery(opts = {}) {
  const shouldClear = !!opts.forceClear || !(state.listMode === 'infinite' && state.page > 1);
  if (shouldClear) {
    galleryEl.innerHTML = '';
  }
  // 更新右下角页码显示
  if (fcNum) {
    fcNum.textContent = String(state.page);
  }
  const existingIds = new Set(Array.from(galleryEl.querySelectorAll('.card img')).map((img) => Number(img.dataset.workId)));
  const baseItems = shouldClear ? state.items : state.items.filter((w) => !existingIds.has(w.id));
  const renderItems = visibleWorks(baseItems);
  const adAfterVisibleCount = Math.max(1, getGalleryColumnCount() * 3);
  const visibleCountByPage = new Map();
  renderItems.forEach((w, index) => {
    const card = document.createElement('div');
    card.className = 'card';
    // thumbnail uses actual image address; pick first image via work detail fetch when hover
    const img = document.createElement('img');
    img.loading = 'lazy';
    img.decoding = 'async';
    img.alt = t('thumb_alt');
    img.draggable = false;
    // lazy set src when in viewport via IntersectionObserver fallback
    img.dataset.workId = w.id;
    card.appendChild(img);

    const cardLink = document.createElement('a');
    cardLink.className = 'card-link';
    cardLink.href = withLangParam(`/i/${encodeURIComponent(String(w.id))}`);
    cardLink.target = '_blank';
    cardLink.rel = 'noopener';
    cardLink.setAttribute('aria-label', (w.title && String(w.title).trim()) ? String(w.title).trim() : t('work_fallback', { id: w.id }));
    cardLink.addEventListener('click', (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      const id = w.id;
      if (state.openWorkInNewWindow) {
        window.open(withLangParam(`/i/${id}`), '_blank', 'noopener');
        return;
      }
      state.directDetail = false;
      openDetail(id);
    });
    card.appendChild(cardLink);

    const badge = document.createElement('div');
    badge.className = 'badge';
    badge.textContent = w.image_count || 0;
    card.appendChild(badge);

    try {
      const mode = (sortModeSel && sortModeSel.value) || (sortModeSel2 && sortModeSel2.value) || 'new';
      if (mode === 'monthly') {
        const mets = document.createElement('div');
        mets.className = 'card-metrics';
        const v = document.createElement('span');
        v.className = 'cm-view';
        v.textContent = `${formatMetric(Number(w.total_view || 0))}V`;
        const b = document.createElement('span');
        b.className = 'cm-bookmark';
        b.textContent = `${formatMetric(Number(w.total_bookmarks || 0))}B`;
        mets.appendChild(v);
        mets.appendChild(b);
        card.appendChild(mets);
      }
    } catch { }

    // 左上角类型徽章（不同颜色）
    const typeBadge = document.createElement('div');
    typeBadge.className = 'type-pill ' + typeClass(w.AI_type || '');
    typeBadge.textContent = String(w.AI_type || '').toUpperCase();
    typeBadge.title = t('type_search_tip');
    typeBadge.addEventListener('click', (e) => {
      e.stopPropagation();
      const url = `/?q=${encodeURIComponent(String(w.AI_type || ''))}`;
      window.open(withLangParam(url), '_blank', 'noopener');
    });
    card.appendChild(typeBadge);

    const meta = document.createElement('div');
    meta.className = 'meta';
    const workHref = withLangParam(`/i/${encodeURIComponent(String(w.id))}`);
    const titleText = (w.title && String(w.title).trim()) ? String(w.title).trim() : '';
    const titlePart = titleText ? `<div class="meta-title"><a class="meta-link" href="${escapeHtml(workHref)}" target="_blank" rel="noopener">${escapeHtml(titleText)}</a></div>` : '';
    // 移动端简介仅显示 10 个字符；PC 端保持较长（70）；移动端判定扩展为 ≤800px
    const isMobile = window.innerWidth <= 800;
    const capPart = w.caption ? `<div class="meta-caption">${escapeHtml(snippet(w.caption, isMobile ? 10 : 70))}</div>` : '';
    const dateStr = w.create_date ? formatDate(w.create_date) : '';
    const datePart = dateStr ? `<div class="meta-date"><a class="meta-link" href="${escapeHtml(workHref)}" target="_blank" rel="noopener">${escapeHtml(dateStr)}</a></div>` : '';
    meta.innerHTML = `${titlePart}${capPart}${datePart}`;
    try {
      const links = meta.querySelectorAll('.meta-link');
      links.forEach((a) => {
        a.addEventListener('click', (ev) => {
          ev.stopPropagation();
        });
      });
    } catch { }
    card.appendChild(meta);

    if (shouldEnableHoverPreview()) {
      card.addEventListener('mouseenter', () => openPreview(w.id, card));
      card.addEventListener('mouseleave', () => closePreview());
    }
    card.addEventListener('click', () => {
      const id = w.id;
      if (state.openWorkInNewWindow) {
        window.open(withLangParam(`/i/${id}`), '_blank', 'noopener');
        return;
      }
      state.directDetail = false;
      openDetail(id);
    });

	    galleryEl.appendChild(card);
    const listPage = getWorkListPage(w);
    const nextCount = (visibleCountByPage.get(listPage) || 0) + 1;
    visibleCountByPage.set(listPage, nextCount);
    if (nextCount === adAfterVisibleCount) {
      appendGalleryAd(`page-${listPage}-after-3-rows`);
    }
	  });

	  // 保证哨兵始终位于末尾
  const sentinel = document.getElementById('infiniteSentinel');
  if (sentinel && state.listMode === 'infinite') {
    galleryEl.appendChild(sentinel);
  }

	  // load first images of each work for thumbnails
	  const cards = galleryEl.querySelectorAll('.card img');
	  cards.forEach(async (img) => {
	    if (img.src) return; // 已加载的缩略图不重复请求详情
	    const workId = img.dataset.workId;
	    try {
	      const cacheKey = normalizeWorkId(workId);
	      let data = state.cache.works.get(cacheKey);
	      if (!data) {
	        const res = await fetch(`${API_BASE}/api/work/${workId}`);
	        if (!res.ok) return;
	        data = await res.json();
	        // 缓存作品详情，避免重复请求
	        state.cache.works.set(cacheKey, data);
	      }
	      const flagsChanged = rememberWorkFlagsFromDetail(data);
	      const detailWork = (data && data.work) || { id: workId };
	      if (flagsChanged && isFrontendHiddenWork(detailWork)) {
	        scheduleFrontendFilterRefresh();
	        return;
	      }
	      try {
	        const wtype = String((data.work || {}).AI_type || '').toLowerCase();
	        if ((wtype === 'nai' || wtype === 'nai_x') && window.NAIX && typeof window.NAIX.suspectWork === 'function') {
	          const isSuspect = !!getWorkFlags(workId).suspectInvalidTags;
	          if (isSuspect) {
	            const cardEl = img.parentElement;
	            if (cardEl && !cardEl.querySelector('.type-pill.naix-flag')) {
              const flag = document.createElement('div');
              flag.className = 'type-pill naix-flag';
              flag.textContent = t('naix_suspect');
              // 放置在 NAI 徽章右侧
              try {
                const baseBadge = cardEl.querySelector('.type-pill.nai') || cardEl.querySelector('.type-pill');
                if (baseBadge) {
                  const rect = baseBadge.getBoundingClientRect();
                  const parentRect = cardEl.getBoundingClientRect();
                  const left = (rect.left - parentRect.left) + baseBadge.offsetWidth + 6;
                  flag.style.left = `${left}px`;
                  flag.style.top = `${baseBadge.offsetTop}px`;
                }
              } catch { }
              cardEl.appendChild(flag);
            }
          }
        }
        if (wtype === 'comfyui' && isNonStandardComfyuiWork(data)) {
          const cardEl = img.parentElement;
          if (cardEl && !cardEl.querySelector('.type-pill.nonstandard-flag')) {
            const flag = document.createElement('div');
            flag.className = 'type-pill naix-flag nonstandard-flag';
            flag.textContent = t('non_standard_format');
            flag.title = t('non_standard_format_tip');
            try {
              const baseBadge = cardEl.querySelector('.type-pill.comfyui') || cardEl.querySelector('.type-pill');
              if (baseBadge) {
                const rect = baseBadge.getBoundingClientRect();
                const parentRect = cardEl.getBoundingClientRect();
                const left = (rect.left - parentRect.left) + baseBadge.offsetWidth + 6;
                flag.style.left = `${left}px`;
                flag.style.top = `${baseBadge.offsetTop}px`;
              }
            } catch { }
            cardEl.appendChild(flag);
          }
        }
      } catch { }
      // 选择排序后的第一张作为缩略图
      const first = (data.images || []).slice().sort((a, b) => getPageIndex(a) - getPageIndex(b))[0];
      if (first) {
        img.src = buildImageUrl(first);
      }
      // 以详情返回的图片数为准，回填右上角徽章，避免列表缺失计数
      try {
        const badgeEl = img.parentElement.querySelector('.badge');
        if (badgeEl) {
          const cnt = (data.images || []).length;
          badgeEl.textContent = String(cnt || 0);
        }
      } catch { }
    } catch { }
  });
}

let infiniteObserver = null;
function setupInfiniteScroll() {
  let sentinel = document.getElementById('infiniteSentinel');
  if (!sentinel) {
    sentinel = document.createElement('div');
    sentinel.id = 'infiniteSentinel';
    sentinel.style.height = '1px';
    sentinel.style.margin = '0';
    sentinel.style.visibility = 'hidden';
  }
  // 始终把哨兵置于末尾
  galleryEl.appendChild(sentinel);
  // 每次调用都重新注册观察器，避免旧观察器状态导致只触发一次
  if (infiniteObserver) {
    try { infiniteObserver.disconnect(); } catch { }
    infiniteObserver = null;
  }
  infiniteObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        const totalPages = Math.max(1, Math.ceil((state.total || 0) / (state.pageSize || 1)));
        const unknownTotal = (state.total <= 0);
        const hasNext = unknownTotal ? (lastPageCount === state.pageSize) : (state.page < totalPages);
        if (hasNext) {
          if (!loadingPage) {
            state.page += 1;
            fetchWorks();
          }
        } else {
          // 无更多数据，注销观察器
          if (infiniteObserver) {
            infiniteObserver.disconnect();
            infiniteObserver = null;
          }
          endReached = true;
          if (loadMoreBtn) loadMoreBtn.classList.add('hidden');
        }
      }
    }
  }, { rootMargin: '400px' });
  infiniteObserver.observe(sentinel);
}

async function fetchWork(workId) {
  if (state.cache.works.has(workId)) {
    return state.cache.works.get(workId);
  }
	  const res = await fetch(`${API_BASE}/api/work/${workId}`);
	  if (!res.ok) throw new Error(t('err_network'));
	  const data = await res.json();
	  state.cache.works.set(workId, data);
	  try { rememberWorkFlagsFromDetail(data); } catch { }
	  return data;
	}

async function openPreview(workId, cardEl) {
  if (!shouldEnableHoverPreview()) return;
  try {
    const data = await fetchWork(workId);
    const images = data.images || [];
    if (!images.length) return;
    // 预览按文件名中的 _pN 升序排序
    const sorted = images.slice().sort((a, b) => getPageIndex(a) - getPageIndex(b));
    state.preview.images = sorted.map((i) => buildImageUrl(i)).filter(Boolean);
    state.preview.index = 0;
    const w = data.work || {};
    hpTitle.textContent = (w.title && String(w.title).trim()) ? w.title : t('work_fallback', { id: workId });
    hpCount.textContent = t('images_count', { n: images.length });
    hpImg.src = state.preview.images[0];

    // 计算预览面板位置（左/右侧 + 顶部跟随卡片）
    const rect = cardEl.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    state.preview.side = centerX < window.innerWidth / 2 ? 'right' : 'left';
    state.preview.anchorEl = cardEl;
    // 等图片加载后再定位，获取真实高度以便决定上下显示
    hpImg.onload = () => { if (state.preview.active) positionHoverPreview(); };
    positionHoverPreview();
    state.preview.active = true;
    hoverPreview.classList.remove('hidden');
  } catch { }
}

function positionHoverPreview() {
  const anchor = state.preview.anchorEl;
  if (!anchor) return;
  const rect = anchor.getBoundingClientRect();
  const gap = parseFloat(getComputedStyle(galleryEl).gap || '12') || 12;
  // 目标高度：约两卡高
  const targetH = rect.height * 2 + gap;
  const ar = (hpImg.naturalWidth && hpImg.naturalHeight) ? (hpImg.naturalWidth / hpImg.naturalHeight) : 1.6;
  const desiredWidth = Math.max(rect.width * 2 + gap, Math.ceil(targetH * ar));
  const maxWidth = Math.min(desiredWidth, window.innerWidth - 32);
  hoverPreview.style.width = `${maxWidth}px`;
  // 限制图片最大高度为两卡高（再夹紧到视口）
  const maxImgH = Math.min(targetH, window.innerHeight - 160);
  hpImg.style.maxHeight = `${maxImgH}px`;

  // 计算预览高度（包含头部），用于上下判断
  const pvRect = hoverPreview.getBoundingClientRect();
  const pvH = Math.max(pvRect.height, maxImgH + 56); // 预估头部高度 + 内边距
  const spaceAbove = rect.top - 16;
  const spaceBelow = window.innerHeight - rect.bottom - 16;
  // 优先选择空间更充足的一侧；若下方不足，则放到上方
  let top;
  if (spaceBelow < pvH && spaceAbove >= 100) {
    // 放到卡片上方
    top = rect.top - pvH - gap;
  } else {
    // 放到卡片下方或同一水平线上（顶部对齐）
    top = Math.max(16, rect.top);
  }
  // 夹紧到视口
  const maxTop = window.innerHeight - pvH - 16;
  hoverPreview.style.top = `${Math.max(16, Math.min(top, maxTop))}px`;

  // 左右位置紧贴卡片侧边，并避免溢出
  let left;
  if (state.preview.side === 'right') {
    left = rect.right + gap;
    if (left + maxWidth + 16 > window.innerWidth) {
      state.preview.side = 'left';
      left = rect.left - gap - maxWidth;
    }
  } else {
    left = rect.left - gap - maxWidth;
    if (left < 16) {
      state.preview.side = 'right';
      left = rect.right + gap;
    }
  }
  left = Math.max(16, Math.min(left, window.innerWidth - maxWidth - 16));
  hoverPreview.style.left = `${left}px`;
}

function closePreview() {
  state.preview.active = false;
  hoverPreview.classList.add('hidden');
}

// 在详情页内平滑滚动到指定 JSON 框，考虑粘性头部的高度
function scrollJsonIntoView(boxEl) {
  try {
    const headerEl = detailView.querySelector('.detail-header');
    const offset = headerEl ? headerEl.offsetHeight : 0;
    const top = Math.max(0, boxEl.offsetTop - offset - 8);
    detailView.scrollTo({ top, behavior: 'smooth' });
  } catch {
    try { boxEl.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'nearest' }); } catch { }
  }
}

function getDetailScrollKey(workId) {
  return String(normalizeWorkId(workId));
}

function clearDetailScrollRestoreTimers() {
  try {
    (state.detailScroll.restoreTimers || []).forEach((timer) => clearTimeout(timer));
    state.detailScroll.restoreTimers = [];
  } catch { }
}

function saveCurrentDetailScroll() {
  try {
    if (!detailView || detailView.classList.contains('hidden')) return;
    const key = state.detailScroll.currentWorkId;
    if (!key) return;
    state.detailScroll.byWork.set(key, Math.max(0, Math.round(detailView.scrollTop || 0)));
  } catch { }
}

function restoreDetailScrollForWork(workId) {
  const key = getDetailScrollKey(workId);
  const hasSavedScroll = state.detailScroll.byWork.has(key);
  const y = hasSavedScroll ? Number(state.detailScroll.byWork.get(key) || 0) : 0;
  const apply = () => {
    try {
      if (state.detailScroll.currentWorkId !== key) return;
      state.detailScroll.isRestoring = true;
      detailView.scrollTo({ top: Math.max(0, y), behavior: 'auto' });
      setTimeout(() => { state.detailScroll.isRestoring = false; }, 50);
    } catch {
      try { detailView.scrollTop = Math.max(0, y); } catch { }
      state.detailScroll.isRestoring = false;
    }
  };
  clearDetailScrollRestoreTimers();
  try { requestAnimationFrame(apply); } catch { apply(); }
  if (!hasSavedScroll || y <= 0) return;
  // 图片加载会改变详情页高度，多补几次定位，避免恢复位置被布局变化吞掉。
  try {
    state.detailScroll.restoreTimers = [80, 280, 900].map((delay) => setTimeout(apply, delay));
  } catch { }
}

let detailScrollSaveRaf = 0;
if (detailView) {
  detailView.addEventListener('scroll', () => {
    if (detailScrollSaveRaf) return;
    detailScrollSaveRaf = requestAnimationFrame(() => {
      detailScrollSaveRaf = 0;
      if (!state.detailScroll.isRestoring) {
        clearDetailScrollRestoreTimers();
      }
      saveCurrentDetailScroll();
    });
  }, { passive: true });
}

// 键盘翻页
window.addEventListener('keydown', (e) => {
  if (!state.preview.active) return;
  if (e.key === 'ArrowRight' || e.key === 'PageDown') {
    if (state.preview.images.length) {
      state.preview.index = (state.preview.index + 1) % state.preview.images.length;
      hpImg.src = state.preview.images[state.preview.index];
    }
  } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
    if (state.preview.images.length) {
      state.preview.index = (state.preview.index - 1 + state.preview.images.length) % state.preview.images.length;
      hpImg.src = state.preview.images[state.preview.index];
    }
  } else if (e.key === 'Escape') {
    closePreview();
  }
});

// 在预览激活时拦截滚轮，防止页面滚动，并实现图片翻页
function onWheel(e) {
  if (!state.preview.active) return;
  e.preventDefault();
  e.stopPropagation();
  const len = state.preview.images.length;
  if (!len) return;
  const dir = e.deltaY > 0 ? 1 : -1;
  state.preview.index = (state.preview.index + dir + len) % len;
  hpImg.src = state.preview.images[state.preview.index];
}
window.addEventListener('wheel', onWheel, { passive: false });

// 在滚动或窗口尺寸变化时，预览面板跟随卡片重新定位
window.addEventListener('resize', () => {
  if (!shouldEnableHoverPreview()) {
    if (state.preview.active) closePreview();
    return;
  }
  if (state.preview.active) positionHoverPreview();
});
window.addEventListener('scroll', () => { if (state.preview.active) positionHoverPreview(); }, { passive: true });

async function openDetail(workId) {
  saveCurrentDetailScroll();
  state.detailScroll.currentWorkId = getDetailScrollKey(workId);
  history.pushState({ view: 'detail', workId }, '', withLangParam(`/i/${workId}`));
  try {
    const data = await fetchWork(workId);
    try {
      const authorId = Number((data.work || {}).userId);
      const cfg = await getConfig();
      const blob = cfg.blacklist_authors_blob || {};
      const set = await decodeBlacklistSet(blob);
      if (set.size && !Number.isNaN(authorId) && set.has(authorId)) {
        detailView.classList.add('blocked-detail');
        try { history.pushState({ view: 'list' }, '', withLangParam('/')); } catch { }
        return;
      }
    } catch { }
    const w = data.work || {};
    const nonStandardComfy = isNonStandardComfyuiWork(data);
    try { applyWorkSeo(workId, w, data.images || []); } catch { }
    detailTitle.textContent = (w.title && String(w.title).trim()) ? w.title : t('work_fallback', { id: workId });
    // 直达详情页：在标题左侧添加可点击返回首页的图标
    try {
      const detailHeader = document.querySelector('.detail-header');
      let homeLink = document.getElementById('detailHomeLink');
      if (state.directDetail) {
        if (!homeLink && detailHeader) {
          homeLink = document.createElement('a');
          homeLink.id = 'detailHomeLink';
          homeLink.className = 'home-link';
          homeLink.href = withLangParam('/');
          homeLink.title = t('home_title');
          const img = document.createElement('img');
          img.src = '/favicon.ico';
          img.alt = t('home_alt');
          homeLink.appendChild(img);
          // 插入到标题之前
          detailHeader.insertBefore(homeLink, detailTitle);
        }
        if (homeLink) homeLink.style.display = '';
      } else {
        if (homeLink) homeLink.remove();
      }
    } catch { }
    const authorLink = w.userId ? `<a class="chip" href="${escapeHtml(withLangParam(`/?q=${encodeURIComponent(String(w.userId))}`))}" target="_blank" rel="noopener">${escapeHtml(String(w.userId))}</a>` : '';
    let typeLink = w.AI_type ? `<a class="chip ${typeClass(w.AI_type)}" href="${escapeHtml(withLangParam(`/?q=${encodeURIComponent(String(w.AI_type))}`))}" target="_blank" rel="noopener">${escapeHtml(String(w.AI_type))}</a>` : '';
    const tags = normalizeTags(w.tags);
    // 标签链接需要双引号包裹值：/?q="标签"
    const tagLinks = tags.map((tag) => {
      const q = `"${String(tag)}"`;
      const url = withLangParam(`/?q=${encodeURIComponent(q)}`);
      return `<a class="chip" href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(tag)}</a>`;
    }).join(' ');
    const nonStandardTipHtml = nonStandardComfy ? `
    <div class="dm-row nonstandard-tip-row"><span class="nonstandard-tip">${escapeHtml('*' + t('non_standard_format_tip'))}</span></div>
  ` : '';
    const captionHtml = w.caption ? `
    <div class="dm-row">${escapeHtml(t('dm_caption'))}:</div>
    <div class="dm-caption collapsed" id="dmCaption">${renderCaption(w.caption)}</div>
    <div class="caption-toggle-row"><button id="captionToggleBtn" class="btn outline caption-toggle-btn">${escapeHtml(t('caption_show_all'))}</button></div>
  ` : '';
    const postedStr = w.create_date ? formatDateTime(w.create_date) : '';
    detailMeta.innerHTML = `
      <div class="dm-title">${escapeHtml((w.title && String(w.title).trim()) ? w.title : t('work_fallback', { id: workId }))}</div>
      <div class="dm-row">${escapeHtml(t('dm_pixiv_id'))}: <a class="chip" href="https://www.pixiv.net/artworks/${workId}" target="_blank" rel="noopener">${escapeHtml(String(workId))}</a></div>
      <div class="dm-row">${escapeHtml(t('dm_author'))}: ${authorLink || escapeHtml(t('dm_unknown'))}</div>
      <div class="dm-row">${escapeHtml(t('dm_type'))}: ${typeLink || escapeHtml(t('dm_unknown'))}</div>
      ${nonStandardTipHtml}
      <div class="dm-row">${escapeHtml(t('dm_tags'))}: ${tagLinks || `<span class="no-tags">${escapeHtml(t('dm_none'))}</span>`}</div>
      ${captionHtml}
      <div class="dm-row">${escapeHtml(t('dm_posted_at'))}: ${postedStr ? escapeHtml(postedStr) : escapeHtml(t('dm_unknown'))}</div>
      <div class="dm-row small">${escapeHtml(t('dm_views'))}: ${w.total_view ?? ''} · ${escapeHtml(t('dm_bookmarks'))}: ${w.total_bookmarks ?? ''}</div>
      ${String(w.AI_type || '').toLowerCase() === 'nai' ? `
      <div class="ai-mode-row">
        <span class="ai-mode-label">${escapeHtml(t('ai_meta_mode'))}:</span>
        <div class="ai-mode-toggle" id="aiModeToggle" data-mode="json">
          <div class="ai-toggle">
            <span class="toggle-text left">json</span>
            <span class="toggle-text right">${escapeHtml(t('copy_instruction'))}</span>
            <div class="knob"></div>
            <div class="hit hit-left" data-value="json"></div>
            <div class="hit hit-right" data-value="instruction"></div>
          </div>
        </div>
      </div>` : ''}
      <div class="download-row">
        <button id="downloadAllBtn" class="btn">${escapeHtml(t('copy_all_image_links'))}</button>
      </div>
    `;
    try {
      const downloadRow = detailMeta.querySelector('.download-row');
      const detailAd = createAdElement('detail');
      if (downloadRow && detailAd) {
        detailAd.dataset.insertSlot = 'detail';
        downloadRow.after(detailAd);
      }
    } catch { }
    // 简介折叠/展开按钮逻辑：默认折叠为 5 行，溢出时显示按钮
    try {
      const captionEl = document.getElementById('dmCaption');
      const toggleBtn = document.getElementById('captionToggleBtn');
      if (captionEl && toggleBtn) {
        requestAnimationFrame(() => {
          const overflow = captionEl.scrollHeight > captionEl.clientHeight + 1;
          toggleBtn.style.display = overflow ? '' : 'none';
        });
        toggleBtn.addEventListener('click', () => {
          const collapsed = captionEl.classList.contains('collapsed');
          captionEl.classList.toggle('collapsed', !collapsed);
          toggleBtn.textContent = collapsed ? t('caption_collapse') : t('caption_show_all');
        });
      }
    } catch { }
    const downloadAllBtn = document.getElementById('downloadAllBtn');
    const aiModeToggle = document.getElementById('aiModeToggle');
    // 根据进入方式控制返回按钮显示
    backBtn.style.display = state.directDetail ? 'none' : '';
    // 重置本作品的 JSON 框注册与状态
    detailJsonBoxes = [];
    detailJsonExpanded = false;
    detailImages.innerHTML = '';
    // 详情页图片按 _pN 升序排序
    (data.images || []).slice().sort((a, b) => getPageIndex(a) - getPageIndex(b)).forEach((img) => {
      const card = document.createElement('div');
      card.className = 'img-card';
      const imageEl = document.createElement('img');
      imageEl.loading = 'lazy';
      imageEl.src = buildImageUrl(img);
      card.appendChild(imageEl);
      // 每张图片的 AI JSON 独立显示框（折叠态统一可见高度，框内半透明按钮）
      const jsonBox = document.createElement('div');
      jsonBox.className = 'json-box';
      // 初始为折叠态，统一高度由样式控制
      jsonBox.classList.add('collapsed');
      // 根据作品 AI 类型为 JSON 框附加类名（sd/nai/comfyui），以便差异化颜色
      try {
        const wtype = (data.work || {}).AI_type || '';
        const cls = typeClass(wtype);
        if (cls) jsonBox.classList.add(cls);
      } catch { }
      let pretty = '';
      let objForDetection = null;
      try {
        const obj = typeof img.ai_json === 'string' ? JSON.parse(img.ai_json) : img.ai_json || {};
        objForDetection = obj;
        pretty = JSON.stringify(obj, null, 2);
      } catch {
        pretty = String(img.ai_json || '');
      }
      const copyJsonText = String(pretty);

      // --- 限制显示长度（100KB），过长则截断并提示 ---
      const MAX_DISPLAY_LEN = 100 * 1024; // 100KB
      let displayText = copyJsonText;
      let isTruncated = false;
      if (displayText.length > MAX_DISPLAY_LEN) {
        displayText = displayText.slice(0, MAX_DISPLAY_LEN) + '\n\n... (AI metadata too large, truncated) ...';
        isTruncated = true;
      }

      const displayHtml = syntaxHighlight(displayText.replace(/\\n/g, '\n'));
      const fullHtml = syntaxHighlight(copyJsonText.replace(/\\n/g, '\n')); // 完整版 HTML (用于“显示完整”时切换)

      const preEl = document.createElement('pre');
      preEl.className = 'json-content';
      preEl.innerHTML = displayHtml;

      const actionsEl = document.createElement('div');
      actionsEl.className = 'json-actions';

      // 如果被截断，添加“显示完整”按钮
      if (isTruncated) {
        const loadFullBtn = document.createElement('button');
        loadFullBtn.className = 'btn ghost';
        loadFullBtn.textContent = t('show_full_meta') || 'Show Full Metadata';
        loadFullBtn.style.marginRight = '8px';
        loadFullBtn.onclick = () => {
          preEl.innerHTML = fullHtml;
          loadFullBtn.remove(); // 点击后移除自身
          // 重新判断高度逻辑（因为内容变长了）
          setTimeout(() => checkHeight(), 50);
        };
        actionsEl.appendChild(loadFullBtn);
      }

      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn ghost';
      copyBtn.textContent = t('copy_json');
      // 为后续指令切换准备原始/指令文本
      jsonBox._fullText = copyJsonText;
      jsonBox._fullHtml = fullHtml;
      let instructionText = '';
      try {
        if (jsonBox.classList.contains('nai') && window.NAI && typeof window.NAI.convert === 'function') {
          const res = window.NAI.convert(objForDetection || {});
          instructionText = (res && res.txt) ? String(res.txt) : '';
        }
      } catch { }
      jsonBox._instructionText = instructionText || copyJsonText;
      copyBtn.dataset.mode = 'json';
      // 复制：根据当前模式复制 JSON 或 指令
      copyBtn.addEventListener('click', async () => {
        const mode = copyBtn.dataset.mode || 'json';
        const text = mode === 'instruction' ? (jsonBox._instructionText || '') : (jsonBox._fullText || '');
        let copied = false;
        try {
          await navigator.clipboard.writeText(text);
          copied = true;
        } catch (e) {
          // Safari/iOS 等环境降级：使用隐藏 textarea + execCommand('copy')
          try {
            const ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.top = '-1000px';
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            copied = document.execCommand('copy');
            document.body.removeChild(ta);
            if (!copied) {
              alert(t('copy_failed_manual') + text);
            }
          } catch {
            alert(t('copy_failed_manual') + text);
          }
        }
        copyBtn.textContent = copied ? t('copied') : t('copy_failed');
        setTimeout(() => { copyBtn.textContent = (mode === 'instruction' ? t('copy_instruction') : t('copy_json')); }, 1500);
      });
      actionsEl.appendChild(copyBtn);
      jsonBox.appendChild(actionsEl);
      // NAI 模型/类型头部（仅对 NAI 类型图片显示；不参与复制 JSON）
      try {
        const wtypeLower = String((data.work || {}).AI_type || '').toLowerCase();
        if (wtypeLower === 'comfyui' && nonStandardComfy) {
          const headerEl = document.createElement('div');
          headerEl.className = 'json-header';
          const flagEl = document.createElement('span');
          flagEl.className = 'naix-label nonstandard-flag';
          flagEl.textContent = t('non_standard_format_bracket');
          flagEl.title = t('non_standard_format_tip');
          headerEl.appendChild(flagEl);
          jsonBox.appendChild(headerEl);
          jsonBox.classList.add('has-header');
        }
        if ((wtypeLower === 'nai' || wtypeLower === 'nai_x') && window.NAI && typeof window.NAI.detect === 'function') {
          const det = window.NAI.detect(objForDetection || copyJsonText);
          if (det && det.version && det.type) {
            const headerEl = document.createElement('div');
            headerEl.className = 'json-header';
            if (window.NAIX && typeof window.NAIX.suspect === 'function') {
              try {
                const suspect = !!window.NAIX.suspect(objForDetection || copyJsonText);
                if (suspect) {
                  const suspectEl = document.createElement('span');
                  suspectEl.className = 'naix-label';
                  suspectEl.textContent = t('naix_suspect_bracket');
                  headerEl.appendChild(suspectEl);
                }
              } catch { }
            }
            const modelEl = document.createElement('span');
            modelEl.className = 'json-header-line model';
            modelEl.textContent = `Model:${det.version}`;
            const typeEl = document.createElement('span');
            typeEl.className = 'json-header-line type';
            typeEl.textContent = `Type:${det.type}`;
            headerEl.appendChild(modelEl);
            headerEl.appendChild(typeEl);
            jsonBox.appendChild(headerEl);
            // 标记有头部，以便样式为内容增加顶部空白（避免遮挡）
            jsonBox.classList.add('has-header');
          }
        }
      } catch { }
      // 底部居中“显示全部/折叠”按钮
      const bottomEl = document.createElement('div');
      bottomEl.className = 'json-bottom';
      const showAllBtn = document.createElement('button');
      showAllBtn.className = 'btn ghost';
      showAllBtn.textContent = t('show_all');
      showAllBtn.addEventListener('click', () => {
        // 切换全局展开/折叠状态，并同步所有 JSON 框样式与按钮文案
        detailJsonExpanded = !detailJsonExpanded;
        detailJsonBoxes.forEach((box) => {
          // 短内容没有按钮，跳过折叠/展开切换
          if (box.btn && box.btn.style.display === 'none') return;
          if (detailJsonExpanded) {
            box.boxEl.classList.remove('collapsed');
            box.btn.textContent = t('collapse');
          } else {
            box.boxEl.classList.add('collapsed');
            box.btn.textContent = t('show_all');
          }
        });
        // 等待布局完成后，将视图定位到触发按钮所在的 JSON 框
        setTimeout(() => scrollJsonIntoView(jsonBox), 0);
      });
      bottomEl.appendChild(showAllBtn);
      jsonBox.appendChild(preEl);
      jsonBox.appendChild(bottomEl);
      card.appendChild(jsonBox);
      // 注册到全局列表，便于统一切换
      detailJsonBoxes.push({ boxEl: jsonBox, preEl, btn: showAllBtn, copyBtn });
      // 根据内容高度决定显示逻辑：短内容收回底部留白并隐藏按钮；长内容保持折叠固定高度
      function checkHeight() {
        try {
          const maxH = 320;
          const h = preEl.scrollHeight; // 实际内容高度
          const isShort = h <= maxH;
          if (isShort) {
            // 短内容：不需要“显示全部”，收回底部留白
            showAllBtn.style.display = 'none';
            bottomEl.style.display = 'none';
            jsonBox.classList.remove('collapsed');
            jsonBox.classList.add('short');
          } else {
            // 长内容：保留固定高度与按钮
            showAllBtn.style.display = '';
            bottomEl.style.display = '';
            jsonBox.classList.remove('short');
            jsonBox.classList.add('collapsed');
          }
        } catch { }
      }
      setTimeout(checkHeight, 0);
      detailImages.appendChild(card);
    });
    try {
      const wtype = String((data.work || {}).AI_type || '').toLowerCase();
      if ((wtype === 'nai' || wtype === 'nai_x') && window.NAIX && typeof window.NAIX.suspectWork === 'function') {
        const isSuspect = !!window.NAIX.suspectWork(data);
        const meta = document.getElementById('detailMeta');
        if (meta) {
          const oldFlag = meta.querySelector('.chip.naix-flag');
          if (oldFlag) oldFlag.remove();
        }
        if (isSuspect && meta) {
          const typeChip = meta.querySelector('.chip.nai');
          if (typeChip) {
            const flag = document.createElement('span');
            flag.className = 'chip naix-flag';
            flag.textContent = t('naix_suspect_paren');
            typeChip.after(flag);
          }
        }
      }
    } catch { }
    try {
      const wtype = String((data.work || {}).AI_type || '').toLowerCase();
      const meta = document.getElementById('detailMeta');
      if (meta) {
        const oldFlag = meta.querySelector('.chip.nonstandard-flag');
        if (oldFlag) oldFlag.remove();
      }
      if (wtype === 'comfyui' && meta && isNonStandardComfyuiWork(data)) {
        const typeChip = meta.querySelector('.chip.comfyui');
        if (typeChip) {
          const flag = document.createElement('span');
          flag.className = 'chip naix-flag nonstandard-flag';
          flag.textContent = t('non_standard_format_paren');
          flag.title = t('non_standard_format_tip');
          typeChip.after(flag);
        }
      }
    } catch { }
    // AI元数据模式：json / 指令，全局持久化（ON/OFF样式开关）
    if (aiModeToggle) {
      const getStoredMode = () => {
        const v = localStorage.getItem('aiMode') || 'json';
        return (v === 'instruction') ? 'instruction' : 'json';
      };
      const setStoredMode = (m) => { try { localStorage.setItem('aiMode', m); } catch { } };
      const applyModeToBoxes = (mode) => {
        detailJsonBoxes.forEach((box) => {
          try {
            if (!box || !box.boxEl || !box.preEl) return;
            if (!box.boxEl.classList.contains('nai')) return; // 仅 NAI 切换
            if (mode === 'instruction') {
              box.preEl.textContent = box.boxEl._instructionText || '';
              if (box.copyBtn) { box.copyBtn.textContent = t('copy_instruction'); box.copyBtn.dataset.mode = 'instruction'; }
            } else {
              box.preEl.innerHTML = box.boxEl._fullHtml || '';
              if (box.copyBtn) { box.copyBtn.textContent = t('copy_json'); box.copyBtn.dataset.mode = 'json'; }
            }
          } catch { }
        });
      };
      // 初始化：根据 localStorage 设置开关与内容
      let currentMode = getStoredMode();
      const toggleEl = aiModeToggle.querySelector('.ai-toggle');
      const setUi = (m) => { aiModeToggle.setAttribute('data-mode', m); };
      setUi(currentMode);
      applyModeToBoxes(currentMode);
      const onSelect = (m) => {
        if (m === currentMode) return;
        currentMode = m;
        setUi(currentMode);
        setStoredMode(currentMode);
        applyModeToBoxes(currentMode);
      };
      if (toggleEl) {
        const leftHit = aiModeToggle.querySelector('.hit-left');
        const rightHit = aiModeToggle.querySelector('.hit-right');
        const handleByPosition = (e) => {
          try {
            const rect = toggleEl.getBoundingClientRect();
            const x = (e.clientX ?? 0) - rect.left;
            const targetMode = x < rect.width / 2 ? 'json' : 'instruction';
            onSelect(targetMode);
          } catch {
            onSelect(currentMode === 'json' ? 'instruction' : 'json');
          }
        };
        // 点击整体，根据左右半区决定模式
        toggleEl.addEventListener('click', (e) => { handleByPosition(e); });
        // 显式左右命中区，避免圆点或文字影响点击
        if (leftHit) leftHit.addEventListener('click', (e) => { e.stopPropagation(); onSelect('json'); });
        if (rightHit) rightHit.addEventListener('click', (e) => { e.stopPropagation(); onSelect('instruction'); });
      }
    }
    // 将当前作品全部图片链接复制到剪贴板（适配 Chrome/Firefox/Safari，含移动端降级方案）
    downloadAllBtn.addEventListener('click', async () => {
      const urls = (data.images || []).slice().sort((a, b) => getPageIndex(a) - getPageIndex(b)).map((img) => buildImageUrl(img)).filter(Boolean);
      if (!urls.length) {
        downloadAllBtn.textContent = t('no_links_to_copy');
        setTimeout(() => { downloadAllBtn.textContent = t('copy_all_image_links'); }, 1500);
        return;
      }
      const text = urls.join('\n');
      let copied = false;
      try {
        await navigator.clipboard.writeText(text);
        copied = true;
      } catch (e) {
        // Safari/iOS 等环境的降级复制方案
        try {
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.top = '-1000px';
          document.body.appendChild(ta);
          ta.focus();
          ta.select();
          copied = document.execCommand('copy');
          document.body.removeChild(ta);
          if (!copied) {
            alert(t('copy_failed_manual') + text);
          }
        } catch {
          alert(t('copy_failed_manual') + text);
        }
      }
      downloadAllBtn.textContent = copied ? t('copied_n_links', { n: urls.length }) : t('copy_failed_popup');
      setTimeout(() => { downloadAllBtn.textContent = t('copy_all_image_links'); }, 2000);
    });
	    detailView.classList.remove('hidden');
    restoreDetailScrollForWork(workId);
	    closePreview();
	  } catch { }
}

backBtn.addEventListener('click', () => {
  saveCurrentDetailScroll();
  state.detailScroll.currentWorkId = null;
  clearDetailScrollRestoreTimers();
  detailView.classList.add('hidden');
  try { applyHomeSeo(); } catch { }
  history.pushState({ view: 'list' }, '', withLangParam('/'));
});

function triggerSearch() {
  // 重置列表与滚动状态
  state.q = qInput.value.trim();
  state.prompt = promptInput.value.trim();
  state.page = 1;
  state.items = [];
  state.total = 0;
  try { state.workPages.clear(); } catch { }
  loadingPage = false;
  endReached = false;
  lastPageCount = 0;
  if (infiniteObserver) { infiniteObserver.disconnect(); infiniteObserver = null; }
  const oldSentinel = document.getElementById('infiniteSentinel');
  if (oldSentinel) oldSentinel.remove();
  const url = new URL(window.location.href);
  if (state.q) url.searchParams.set('q', state.q); else url.searchParams.delete('q');
  if (state.prompt) url.searchParams.set('prompt', state.prompt); else url.searchParams.delete('prompt');
  try {
    const mode = (sortModeSel && sortModeSel.value) || (sortModeSel2 && sortModeSel2.value) || 'new';
    const tr = (timeRangeSel && timeRangeSel.value) || (timeRangeSel2 && timeRangeSel2.value) || (mode === 'monthly' ? 'current' : 'all');
    url.searchParams.set('sort', mode);
    url.searchParams.set('time_range', tr);
  } catch { }
  history.pushState({ view: 'list' }, '', `${url.pathname}?${url.searchParams.toString()}`);
  try { applyHomeSeo(); } catch { }
  // PC端体验：搜索后强制滚动到顶部，便于查看新结果
  try {
    window.scrollTo({ top: 0, behavior: 'instant' });
    // 某些浏览器不支持 'instant'，兜底：
    setTimeout(() => { window.scrollTo(0, 0); }, 0);
  } catch { window.scrollTo(0, 0); }
  try { if (searchStatusEl) searchStatusEl.classList.add('visible'); } catch { }
  fetchWorks();
}
searchBtn.addEventListener('click', triggerSearch);
qInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') triggerSearch(); });
promptInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') triggerSearch(); });
saveBlacklistBtn.addEventListener('click', () => { saveBlacklist(); triggerSearch(); });

window.addEventListener('popstate', (e) => {
  const s = e.state || {};
  const path = window.location.pathname || '/';
  if (path.startsWith('/i/')) {
    const idStr = path.slice(3);
    const id = parseInt(idStr, 10);
    if (!Number.isNaN(id)) {
      openDetail(id);
      return;
    }
  }
  saveCurrentDetailScroll();
  state.detailScroll.currentWorkId = null;
  clearDetailScrollRestoreTimers();
  detailView.classList.add('hidden');
  try { applyHomeSeo(); } catch { }
  initFromQuery();
});

async function loadConfig() {
  try {
    const res = await fetch(`${API_BASE}/api/config?v=${CONFIG_REQUEST_VERSION}`);
    if (res.ok) {
      let data = {};
      try { data = await res.json(); } catch { data = {}; }
	      CONFIG = { ...CONFIG, ...data };
	      state.pageSize = CONFIG.page_size || state.pageSize;
	      state.listMode = CONFIG.list_mode || 'infinite';
	      scheduleSearchAdPreload();
	      const years = Array.isArray(data.available_years) ? data.available_years : [];
      const months = Array.isArray(data.available_months) ? data.available_months : [];
      if (sortModeSel && sortModeSel.value === 'monthly') {
        rebuildMonthlyOptions(months);
      } else {
        rebuildTimeOptions();
      }
      if (timeRangeSel2 && timeRangeSel) timeRangeSel2.innerHTML = timeRangeSel.innerHTML;
      if (sortModeSel && timeRangeSel) {
        sortModeSel.addEventListener('change', () => {
          const mode = sortModeSel.value || 'new';
          if (mode === 'monthly') {
            const now = new Date(); const y = now.getFullYear(); const m = String(now.getMonth() + 1).padStart(2, '0');
            rebuildMonthlyOptions(months);
            timeRangeSel.value = `m${y}-${m}`;
            if (sortModeSel2) sortModeSel2.value = mode;
            if (timeRangeSel2) timeRangeSel2.value = timeRangeSel.value;
          } else {
            rebuildTimeOptions();
            timeRangeSel.value = 'all';
            if (sortModeSel2) sortModeSel2.value = mode;
            if (timeRangeSel2) timeRangeSel2.value = timeRangeSel.value;
          }
          triggerSearch();
        });
      }
      if (sortModeSel2 && timeRangeSel2) {
        sortModeSel2.addEventListener('change', () => {
          const mode = sortModeSel2.value || 'new';
          if (sortModeSel) sortModeSel.value = mode;
          if (mode === 'monthly') {
            const now = new Date(); const y = now.getFullYear(); const m = String(now.getMonth() + 1).padStart(2, '0');
            rebuildMonthlyOptions(months);
            timeRangeSel2.value = `m${y}-${m}`;
            if (timeRangeSel) timeRangeSel.value = timeRangeSel2.value;
          } else {
            rebuildTimeOptions();
            timeRangeSel2.value = 'all';
            if (timeRangeSel) timeRangeSel.value = timeRangeSel2.value;
          }
          triggerSearch();
        });
      }
      if (timeRangeSel) {
        timeRangeSel.addEventListener('change', () => {
          if (timeRangeSel2) timeRangeSel2.value = timeRangeSel.value;
          triggerSearch();
        });
      }
      if (timeRangeSel2) {
        timeRangeSel2.addEventListener('change', () => {
          if (timeRangeSel) timeRangeSel.value = timeRangeSel2.value;
          triggerSearch();
        });
      }
      // Populate homepage announcement
      try {
        const annZh = String(data.homepage_announcement_zh || '').trim();
        const annEn = String(data.homepage_announcement_en || '').trim();
        const annEl = document.getElementById('heroAnnouncement');
        const annZhEl = document.getElementById('heroAnnouncementZh');
        const annEnEl = document.getElementById('heroAnnouncementEn');
        if (annEl && (annZh || annEn)) {
          if (annZhEl) annZhEl.textContent = annZh;
          if (annEnEl) annEnEl.textContent = annEn;
          annEl.classList.remove('hidden');
        }
      } catch { }
    }
  } catch { }
}

function applyListMode() {
  if (!paginationEl) return;
  if (state.listMode === 'infinite') {
    paginationEl.style.display = 'none';
    // 切换到无限模式时，清理旧观察器
    if (infiniteObserver) { infiniteObserver.disconnect(); infiniteObserver = null; }
    const oldSentinel = document.getElementById('infiniteSentinel');
    if (oldSentinel) oldSentinel.remove();
    if (loadMoreBtn) {
      loadMoreBtn.classList.remove('hidden');
    }
  } else {
    paginationEl.style.display = 'flex';
    if (infiniteObserver) { infiniteObserver.disconnect(); infiniteObserver = null; }
    const oldSentinel = document.getElementById('infiniteSentinel');
    if (oldSentinel) oldSentinel.remove();
    if (loadMoreBtn) {
      loadMoreBtn.classList.add('hidden');
    }
  }
}

function initFromQuery() {
  const url = new URL(window.location.href);
  const q = url.searchParams.get('q') || '';
  const prompt = url.searchParams.get('prompt') || '';
  const pageStr = url.searchParams.get('page');
  const sortModeQ = url.searchParams.get('sort') || 'new';
  const timeRangeQ = url.searchParams.get('time_range') || (sortModeQ === 'monthly' ? 'current' : 'all');
  if (q) state.q = q;
  if (prompt) state.prompt = prompt;
  if (pageStr) {
    const p = parseInt(pageStr, 10);
    if (!Number.isNaN(p) && p >= 1) state.page = p;
  }
  if (sortModeSel) sortModeSel.value = sortModeQ;
  if (sortModeSel2) sortModeSel2.value = sortModeQ;
  if (sortModeSel && sortModeQ === 'monthly') rebuildMonthlyOptions(CONFIG.available_months || []); else rebuildTimeOptions();
  if (timeRangeSel) timeRangeSel.value = timeRangeQ;
  if (timeRangeSel2) timeRangeSel2.value = timeRangeQ;
  qInput.value = state.q;
  promptInput.value = state.prompt;
  if (fcInput) fcInput.value = String(state.page);
  if (fcNum) fcNum.textContent = String(state.page);
  fetchWorks();
}

// initial load
async function initRouter() {
  loadBlacklist();
		  loadOpenWorkInNewWindow();
		  loadInvalidTagFilterSettings();
		  await loadConfig();
  if (oldBlacklistMigrationEnabled()) {
    const importedFromWindow = importBlacklistFromWindowNameIfNeeded();
    const importedFromHash = importBlacklistFromHashIfNeeded();
    if (importedFromWindow || importedFromHash) {
      try { loadBlacklist(); } catch { }
    }
  }
  migrateBlacklistFromOldDomainInBackground();
  try { applyStaticI18n(); } catch { }
  try { applyHomeSeo(); } catch { }
  let seen = false;
  try { seen = localStorage.getItem('announce_seen_v1') === '1'; } catch { }
  if (CONFIG.announce_enabled && !seen && announceOverlay) {
    announceOverlay.classList.remove('hidden');
  }
  const path = window.location.pathname || '/';
  if (path.startsWith('/i/')) {
    const idStr = path.slice(3);
    const id = parseInt(idStr, 10);
    if (!Number.isNaN(id)) {
      state.directDetail = true;
      openDetail(id);
      return;
    }
  }
  state.directDetail = false;
  applyListMode();
  initFromQuery();
}

initRouter();
if (announceClose && announceOverlay) {
  announceClose.addEventListener('click', () => {
    try { localStorage.setItem('announce_seen_v1', '1'); } catch { }
    announceOverlay.classList.add('hidden');
  });
}
	if (openWorkNewWindowToggle) {
	  openWorkNewWindowToggle.addEventListener('change', () => {
	    setOpenWorkInNewWindow(!!openWorkNewWindowToggle.checked);
	  });
	}
	if (showSuspectInvalidTagToggle) {
	  showSuspectInvalidTagToggle.addEventListener('change', () => {
	    setShowSuspectInvalidTags(!!showSuspectInvalidTagToggle.checked);
	  });
	}
	if (showNaixInvalidTagToggle) {
	  showNaixInvalidTagToggle.addEventListener('change', () => {
	    setShowNaixInvalidTags(!!showNaixInvalidTagToggle.checked);
	  });
	}

// 右下角控件逻辑
function toggleHeaderVisibility(show) {
  // 按用户要求：不再隐藏顶部搜索栏，无论何时都保持显示。
  const header = document.querySelector('.site-header');
  if (!header) return;
  const searchRow = header.querySelector('.search-row');
  const blockRow = header.querySelector('.blocklist-row');
  const setRow = (row) => {
    if (!row) return;
    try {
      row.classList.remove('hidden');
      row.style.display = 'flex';
    } catch { }
  };
  setRow(searchRow);
  setRow(blockRow);
}

function applyJumpPage(p) {
  if (Number.isNaN(p) || p < 1) return;
  // 重置瀑布流状态，并从指定页加载
  state.page = p;
  state.items = [];
  endReached = false;
  lastPageCount = 0;
  loadingPage = false;
  // 清空现有内容并重新加载
  galleryEl.innerHTML = '';
  // 清理旧观察器与哨兵
  if (infiniteObserver) { try { infiniteObserver.disconnect(); } catch { } infiniteObserver = null; }
  const oldSentinel = document.getElementById('infiniteSentinel');
  if (oldSentinel) oldSentinel.remove();
  // 更新URL中的page参数，保留现有查询参数
  const url = new URL(window.location.href);
  url.searchParams.set('page', String(p));
  const newUrl = `${url.pathname}${url.search}${url.hash}`;
  history.pushState({ view: 'list' }, '', newUrl);
  // 同步控件显示
  if (fcNum) fcNum.textContent = String(p);
  if (fcInput) fcInput.value = String(p);
  fetchWorks();
}

// 控制搜索栏显示/隐藏的规则：
// - 当搜索栏处于“跟随”或“固定显示”状态时，点击设置芯片不会隐藏搜索栏，只切换面板显示
// - 当搜索栏已经不跟随（用户滚动较远，头部脱离视口）时，点击设置芯片切换显示：显示 -> 隐藏 -> 显示
function isHeaderInViewport() {
  const header = document.querySelector('.site-header');
  if (!header) return true;
  const rect = header.getBoundingClientRect();
  // 顶部贴边或仍在视口内，视为“跟随/固定状态”
  return rect.top >= 0 && rect.bottom > 0;
}

if (fcChip) {
  fcChip.addEventListener('click', () => {
    const panelVisible = !fcPanel.classList.contains('hidden');
    fcPanel.classList.toggle('hidden', panelVisible);
    if (!panelVisible && fcInput) fcInput.focus();

    // 始终保持顶部搜索栏显示（不再隐藏）
    toggleHeaderVisibility(true);

    try {
      if (!panelVisible) {
        const fcQ = document.getElementById('fcQ');
        const fcPrompt = document.getElementById('fcPrompt');
        const fcSearchBtn = document.getElementById('fcSearchBtn');
        const fcBlacklist = document.getElementById('fcBlacklist');
        const fcSaveBlacklistBtn = document.getElementById('fcSaveBlacklistBtn');

        if (fcQ && qInput) fcQ.value = qInput.value || '';
        if (fcPrompt && promptInput) fcPrompt.value = promptInput.value || '';
        if (fcBlacklist && blacklistInput) fcBlacklist.value = blacklistInput.value || '';

        if (fcPanel && !fcPanel.dataset.wired) {
          fcPanel.dataset.wired = '1';
          try {
            if (fcQ && qInput) {
              fcQ.addEventListener('input', () => { try { qInput.value = fcQ.value || ''; } catch { } });
              qInput.addEventListener('input', () => { try { fcQ.value = qInput.value || ''; } catch { } });
            }
          } catch { }
          try {
            if (fcPrompt && promptInput) {
              fcPrompt.addEventListener('input', () => { try { promptInput.value = fcPrompt.value || ''; } catch { } });
              promptInput.addEventListener('input', () => { try { fcPrompt.value = promptInput.value || ''; } catch { } });
            }
          } catch { }
          try {
            if (fcBlacklist && blacklistInput) {
              fcBlacklist.addEventListener('input', () => { try { blacklistInput.value = fcBlacklist.value || ''; } catch { } });
              blacklistInput.addEventListener('input', () => { try { fcBlacklist.value = blacklistInput.value || ''; } catch { } });
            }
          } catch { }
        }

        if (fcSearchBtn) fcSearchBtn.onclick = () => {
          try {
            if (fcQ && qInput) qInput.value = fcQ.value || '';
            if (fcPrompt && promptInput) promptInput.value = fcPrompt.value || '';
          } catch { }
          triggerSearch();
        };
		        if (fcSaveBlacklistBtn) fcSaveBlacklistBtn.onclick = () => {
		          try { if (fcBlacklist && blacklistInput) blacklistInput.value = fcBlacklist.value || ''; } catch { }
		          saveBlacklist();
		          refreshCurrentGallery({ preserveScroll: true });
		        };
      }
    } catch { }
  });
}

if (fcGo && fcInput) {
  fcGo.addEventListener('click', () => {
    const p = parseInt(fcInput.value || '1', 10);
    applyJumpPage(p);
  });
  fcInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const p = parseInt(fcInput.value || '1', 10);
      applyJumpPage(p);
    }
  });
}

function renderPagination() {
  if (!paginationEl) return;
  const totalPages = Math.max(1, Math.ceil((state.total || 0) / (state.pageSize || 1)));
  const groupStart = Math.floor((state.page - 1) / 10) * 10 + 1;
  const groupEnd = Math.min(groupStart + 9, totalPages);

  paginationEl.innerHTML = '';
  paginationEl.style.display = 'flex';

  const makeBtn = (label, page, opts = {}) => {
    const btn = document.createElement('button');
    btn.className = 'page-btn' + (opts.active ? ' active' : '') + (opts.disabled ? ' disabled' : '');
    btn.textContent = label;
    if (!opts.disabled) {
      btn.addEventListener('click', () => {
        if (opts.active) return;
        state.page = page;
        closePreview();
        fetchWorks();
        // 滚动到顶部以便查看新内容
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
    paginationEl.appendChild(btn);
  };

  // 上一组
  if (groupStart > 1) {
    makeBtn(t('prev_group'), groupStart - 10);
  }

  for (let p = groupStart; p <= groupEnd; p++) {
    makeBtn(String(p), p, { active: p === state.page });
  }

  // 下一组
  if (groupEnd < totalPages) {
    makeBtn(t('next_group'), groupEnd + 1);
  }
}

// “加载更多”按钮：在无限模式下作为兜底加载下一页
if (loadMoreBtn) {
  loadMoreBtn.addEventListener('click', () => {
    if (state.listMode !== 'infinite') return;
    const totalPages = Math.max(1, Math.ceil((state.total || 0) / (state.pageSize || 1)));
    if (state.page >= totalPages) {
      loadMoreBtn.classList.add('hidden');
      return;
    }
    if (loadingPage) return;
    state.page += 1;
    fetchWorks();
  });
}
