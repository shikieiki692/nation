# 个人主页 v13.4

# MediaResolver

```jsx
// MediaResolver - 带缓存的媒体文件解析器
const IMG_EXTS = ["webp", "png", "jpg", "jpeg", "svg", "gif"];
const VID_EXTS = ["webm", "mp4", "mov"];

function normalizeVaultPath(input) {
  if (!input) return "";
  let s = String(input).trim();
  s = s.replace(/^\[\[|\]\]$/g, "").replace(/\|.*$/, "").replace(/#.*$/, "");
  s = s.replace(/^\/+/, "").replace(/\\/g, "/").replace(/\/{2,}/g, "/");
  try { s = decodeURIComponent(s); } catch (_) { }
  return s;
}

const MediaResolver = (() => {
  const resourceCache = new Map();
  let filesIndexed = false;
  let fileIndex = null;

  const buildIndex = (dc) => {
    if (filesIndexed) return fileIndex;
    const files = dc.app.vault.getFiles();
    fileIndex = { byName: new Map(), byPath: new Map(), mediaFiles: [] };
    const mediaExts = new Set([...IMG_EXTS, ...VID_EXTS].map(e => e.toLowerCase()));
    files.forEach(file => {
      const nameLower = file.name.toLowerCase();
      const pathLower = file.path.toLowerCase();
      if (!fileIndex.byName.has(nameLower)) fileIndex.byName.set(nameLower, []);
      fileIndex.byName.get(nameLower).push(file);
      fileIndex.byPath.set(pathLower, file);
      const ext = file.extension?.toLowerCase();
      if (ext && mediaExts.has(ext)) fileIndex.mediaFiles.push(file);
    });
    filesIndexed = true;
    return fileIndex;
  };

  const resolveFast = (query, opts = {}, dc) => {
    const index = buildIndex(dc);
    const q = normalizeVaultPath(query);
    if (!q) return null;
    const preferDir = opts.preferDir ? normalizeVaultPath(opts.preferDir).replace(/\/$/, '') : '';
    const preferExts = opts.preferExts || [...IMG_EXTS, ...VID_EXTS];
    const exactFile = index.byPath.get(q.toLowerCase());
    if (exactFile) return exactFile;
    if (preferDir) { const withDir = `${preferDir}/${q}`.toLowerCase(); const dirFile = index.byPath.get(withDir); if (dirFile) return dirFile; }
    const hasExt = /\.[a-z0-9]+$/i.test(q);
    const baseName = hasExt ? q.replace(/\.[^/.]+$/, '') : q;
    const fileName = baseName.split('/').pop();
    const exts = hasExt ? [q.split('.').pop()] : preferExts;
    for (const ext of exts) {
      const fullName = `${fileName}.${ext}`.toLowerCase();
      const candidates = index.byName.get(fullName);
      if (candidates && candidates.length > 0) {
        if (preferDir && candidates.length > 1) { const inPreferredDir = candidates.find(f => f.path.toLowerCase().startsWith(preferDir.toLowerCase())); if (inPreferredDir) return inPreferredDir; }
        return candidates[0];
      }
    }
    return null;
  };

  const resolve = async (query, opts = {}, dc) => {
    if (!query) return null;
    const cacheKey = `${query}|${JSON.stringify(opts)}`;
    if (resourceCache.has(cacheKey)) return resourceCache.get(cacheKey);
    const file = resolveFast(query, opts, dc);
    if (file) { const resourcePath = dc.app.vault.getResourcePath(file); resourceCache.set(cacheKey, resourcePath); return resourcePath; }
    return null;
  };

  const resolveBatch = async (queries, dc) => {
    const results = [];
    buildIndex(dc);
    for (const { query, opts } of queries) {
      const cacheKey = `${query}|${JSON.stringify(opts || {})}`;
      if (resourceCache.has(cacheKey)) { results.push(resourceCache.get(cacheKey)); continue; }
      const file = resolveFast(query, opts, dc);
      if (file) { const resourcePath = dc.app.vault.getResourcePath(file); resourceCache.set(cacheKey, resourcePath); results.push(resourcePath); }
      else results.push(null);
    }
    return results;
  };

  const clearCache = () => { resourceCache.clear(); filesIndexed = false; fileIndex = null; };

  return { resolve, resolveBatch, clearCache, buildIndex };
})();

return { MediaResolver, IMG_EXTS, VID_EXTS, normalizeVaultPath };
```

# ComponentRenderers

```jsx
// ==================== XSS 消毒函数 ====================
const _sanitizeCache = new Map();
const _MAX_CACHE = 200;

// 用于标题：黑名单移除危险标签和事件属性，保留安全的格式化标签
function sanitizeHtml(html) {
  if (!html || typeof html !== 'string') return html || '';
  if (_sanitizeCache.has(html)) return _sanitizeCache.get(html);

  let clean = html;
  // 移除 script 及内容
  clean = clean.replace(/<script[\s>][\s\S]*?<\/script\s*>/gi, '');
  // 移除危险标签（含内容）
  const dangerousTags = ['iframe', 'object', 'embed', 'form', 'link', 'meta', 'base', 'applet', 'frame', 'frameset', 'input', 'textarea', 'select', 'button', 'style', 'head', 'body', 'html'];
  for (const tag of dangerousTags) {
    const re = new RegExp(`<${tag}[^>]*>[\\s\\S]*?<\\/${tag}\\s*>`, 'gi');
    clean = clean.replace(re, '');
    const selfRe = new RegExp(`<${tag}[^>]*/?>`, 'gi');
    clean = clean.replace(selfRe, '');
  }
  // 移除所有 on* 事件属性
  clean = clean.replace(/\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]*)/gi, '');
  // 移除 javascript:/vbscript: URL
  clean = clean.replace(/(href|src|action)\s*=\s*(?:"[^"]*(?:javascript|vbscript)[^"]*"|'[^']*(?:javascript|vbscript)[^']*')/gi, '');
  // 移除 style 中的 expression/url/import
  clean = clean.replace(/style\s*=\s*"[^"]*(?:expression|url\s*\(|@import)[^"]*"/gi, 'style=""');
  clean = clean.replace(/style\s*=\s*'[^']*(?:expression|url\s*\(|@import)[^']*'/gi, "style=''");

  if (_sanitizeCache.size >= _MAX_CACHE) {
    const firstKey = _sanitizeCache.keys().next().value;
    _sanitizeCache.delete(firstKey);
  }
  _sanitizeCache.set(html, clean);
  return clean;
}

// 用于 SVG 图标：验证结构 + 移除危险内容
function sanitizeSvg(svgString) {
  if (!svgString || typeof svgString !== 'string') return '';
  if (_sanitizeCache.has('svg:' + svgString)) return _sanitizeCache.get('svg:' + svgString);

  const trimmed = svgString.trim();
  // 必须以 <svg 开头并以 </svg> 结尾
  if (!/^<svg[\s>]/i.test(trimmed) || !/<\/svg>\s*$/i.test(trimmed)) {
    _sanitizeCache.set('svg:' + svgString, '');
    return '';
  }

  let clean = trimmed;
  // 移除所有 on* 事件属性
  clean = clean.replace(/\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]*)/gi, '');
  // 移除 javascript:/vbscript:/data:text/html URL
  clean = clean.replace(/(href|src|xlink:href)\s*=\s*(?:"[^"]*(?:javascript|vbscript|data\s*:\s*text\/html)[^"]*"|'[^']*(?:javascript|vbscript|data\s*:\s*text\/html)[^']*')/gi, '$1=""');
  // 移除 <script> 标签及内容
  clean = clean.replace(/<script[\s>][\s\S]*?<\/script\s*>/gi, '');
  // 移除 <? ... ?> 处理指令
  clean = clean.replace(/<\?[\s\S]*?\?>/gi, '');
  // 移除 <![CDATA[ ... ]]>
  clean = clean.replace(/<!\[CDATA\[[\s\S]*?\]\]>/gi, '');
  // 移除 <use> 外部引用（防止 SSRF）
  clean = clean.replace(/<use[^>]*(?:href|xlink:href)\s*=\s*["'](?:https?:\/\/|\/\/)[^"']*["'][^>]*>/gi, '');

  if (_sanitizeCache.size >= _MAX_CACHE) {
    const firstKey = _sanitizeCache.keys().next().value;
    _sanitizeCache.delete(firstKey);
  }
  _sanitizeCache.set('svg:' + svgString, clean);
  return clean;
}

// 用于便笺内容：黑名单移除危险标签和事件属性，保留 contentEditable 产生的格式化标签
function sanitizeNoteContent(html) {
  if (!html || typeof html !== 'string') return html || '';
  if (_sanitizeCache.has('note:' + html)) return _sanitizeCache.get('note:' + html);

  let clean = html;
  // 移除 script 及内容
  clean = clean.replace(/<script[\s>][\s\S]*?<\/script\s*>/gi, '');
  // 移除危险标签（含内容）
  const dangerousTags = ['iframe', 'object', 'embed', 'form', 'link', 'meta', 'base', 'applet', 'frame', 'frameset', 'input', 'textarea', 'select', 'button'];
  for (const tag of dangerousTags) {
    const re = new RegExp(`<${tag}[^>]*>[\\s\\S]*?<\\/${tag}\\s*>`, 'gi');
    clean = clean.replace(re, '');
    const selfRe = new RegExp(`<${tag}[^>]*/?>`, 'gi');
    clean = clean.replace(selfRe, '');
  }
  // 移除所有 on* 事件属性
  clean = clean.replace(/\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]*)/gi, '');
  // 移除 javascript:/vbscript: URL
  clean = clean.replace(/(href|src|action)\s*=\s*(?:"[^"]*(?:javascript|vbscript)[^"]*"|'[^']*(?:javascript|vbscript)[^']*')/gi, '');
  // 移除 style 中的 expression/url/import
  clean = clean.replace(/style\s*=\s*"[^"]*(?:expression|url\s*\(|@import)[^"]*"/gi, 'style=""');
  clean = clean.replace(/style\s*=\s*'[^']*(?:expression|url\s*\(|@import)[^']*'/gi, "style=''");

  if (_sanitizeCache.size >= _MAX_CACHE) {
    const firstKey = _sanitizeCache.keys().next().value;
    _sanitizeCache.delete(firstKey);
  }
  _sanitizeCache.set('note:' + html, clean);
  return clean;
}

// ==================== 主题检测与颜色系统 ====================
// 检测 Obsidian 当前是否为深色模式
function isDarkMode() {
  return document.body.classList.contains('theme-dark');
}

// 主题感知颜色系统：根据当前模式返回对应颜色值
// 每个颜色键都有 light 和 dark 两个值
const themeColors = {
  // 基础文本色
  textPrimary:   { light: '#333', dark: '#e0e0e0' },
  textSecondary: { light: '#666', dark: '#aaa' },
  textMuted:     { light: 'rgba(100, 100, 100, 0.7)', dark: 'rgba(160, 160, 160, 0.8)' },
  textFaint:     { light: 'rgba(100, 100, 100, 0.5)', dark: 'rgba(140, 140, 140, 0.6)' },
  textLabel:     { light: '#999', dark: '#888' },

  // 卡片背景色
  cardBg:        { light: '#ffffff', dark: '#2a2a2a' },
  cardBgGlass:   { light: 'rgba(255, 255, 255, 0.4)', dark: 'rgba(40, 40, 40, 0.5)' },
  cardBgGlassHover: { light: 'rgba(255, 255, 255, 0.6)', dark: 'rgba(60, 60, 60, 0.6)' },
  cardBgSubtle:  { light: 'rgba(255, 255, 255, 0.25)', dark: 'rgba(50, 50, 50, 0.35)' },
  cardBgLight:   { light: 'rgba(255, 255, 255, 0.3)', dark: 'rgba(50, 50, 50, 0.4)' },
  cardBgMedium:  { light: 'rgba(255, 255, 255, 0.5)', dark: 'rgba(60, 60, 60, 0.5)' },
  cardBgHeavy:   { light: 'rgba(255, 255, 255, 0.8)', dark: 'rgba(70, 70, 70, 0.8)' },

  // 边框色
  borderLight:   { light: '0.67px solid rgb(255, 255, 255)', dark: '0.67px solid rgba(255, 255, 255, 0.15)' },
  borderDashed:  { light: '2px dashed #667eea', dark: '2px dashed #8b9cf7' },
  borderInput:   { light: '1px solid #ddd', dark: '1px solid #555' },
  borderSubtle:  { light: '1px solid #f0f0f0', dark: '1px solid #3a3a3a' },
  borderPanel:   { light: '1px solid rgba(255,255,255,0.1)', dark: '1px solid rgba(255,255,255,0.08)' },

  // 阴影
  shadowSoft:    { light: '0 0 0 1px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.08)', dark: '0 0 0 1px rgba(255,255,255,0.06), 0 4px 12px rgba(0,0,0,0.3)' },
  shadowGlass:   { light: 'rgba(0, 0, 0, 0.05) 0px 40px 50px -32px, rgba(255, 255, 255, 0.25) 0px 0px 20px 0px inset', dark: 'rgba(0, 0, 0, 0.3) 0px 40px 50px -32px, rgba(255, 255, 255, 0.08) 0px 0px 20px 0px inset' },
  shadowGlassSmall: { light: 'rgba(255, 255, 255, 0.25) 0px 0px 10px 0px inset, rgba(0, 0, 0, 0.05) 0px 4px 10px 0px', dark: 'rgba(255, 255, 255, 0.08) 0px 0px 10px 0px inset, rgba(0, 0, 0, 0.2) 0px 4px 10px 0px' },
  shadowCard:    { light: 'rgb(226, 217, 206) 0px 12px 20px -5px', dark: 'rgba(0, 0, 0, 0.4) 0px 12px 20px -5px' },
  shadowPopup:   { light: '0 4px 12px rgba(0,0,0,0.15)', dark: '0 4px 12px rgba(0,0,0,0.4)' },
  shadowHover:   { light: '0 2px 8px rgba(0,0,0,0.1)', dark: '0 2px 8px rgba(0,0,0,0.3)' },

  // 背景色
  bgInput:       { light: '#fff', dark: '#333' },
  bgPanel:       { light: '#f9f9f9', dark: '#2d2d2d' },
  bgHover:       { light: '#f5f5f5', dark: '#3a3a3a' },
  bgError:       { light: '#fee', dark: 'rgba(245, 87, 108, 0.15)' },

  // 强调色（适配深色的变体）
  accent:        { light: '#667eea', dark: '#8b9cf7' },
  accentHover:   { light: '#5568d3', dark: '#a0b0ff' },
  accentSubtle:  { light: 'rgba(102, 126, 234, 0.1)', dark: 'rgba(139, 156, 247, 0.15)' },
  accentBg:      { light: 'rgba(102, 126, 234, 0.2)', dark: 'rgba(139, 156, 247, 0.2)' },
  accentBgHover: { light: 'rgba(102, 126, 234, 0.3)', dark: 'rgba(139, 156, 247, 0.3)' },

  // 个人面板配色
  nameColor:     { light: 'rgb(51, 79, 82)', dark: 'rgb(200, 220, 225)' },
  taglineColor:  { light: 'rgb(53, 191, 171)', dark: 'rgb(100, 210, 190)' },
  menuFontColor: { light: 'rgb(123, 136, 142)', dark: 'rgb(170, 185, 192)' },
  menuHoverBg:   { light: 'rgba(255, 255, 255, 0.5)', dark: 'rgba(255, 255, 255, 0.08)' },

  // 便笺配色（深色模式变体）
  noteYellowBg:  { light: '#fff394', dark: '#5c5520' },
  noteYellowBorder: { light: '#e6ce5a', dark: '#8a7a30' },
  noteWhiteBg:   { light: '#ffffff', dark: '#3a3a3a' },
  noteWhiteBorder: { light: '#e0e0e0', dark: '#555' },
  noteBrownBg:   { light: '#f9f1e6', dark: '#4a3f30' },
  noteBrownBorder: { light: '#d9b38c', dark: '#8a7050' },
  noteGlassBg:   { light: 'rgba(255, 255, 255, 0.6)', dark: 'rgba(50, 50, 50, 0.6)' },
  noteGlassBorder: { light: 'rgba(255, 255, 255, 0.7)', dark: 'rgba(255, 255, 255, 0.15)' },
  noteGlassInset: { light: 'rgba(255, 255, 255, 0.25) 0px 0px 20px 0px inset', dark: 'rgba(255, 255, 255, 0.05) 0px 0px 20px 0px inset' },
  noteText:      { light: '#222', dark: '#e0e0e0' },
  noteGlassText: { light: '#1f2937', dark: '#e0e0e0' },

  // 编辑弹窗
  editBtnBg:     { light: 'rgba(255, 255, 255, 0.25)', dark: 'rgba(80, 80, 80, 0.5)' },
  editBtnBorder: { light: '0.67px solid rgba(255, 255, 255, 0.5)', dark: '0.67px solid rgba(255, 255, 255, 0.2)' },

  // 拖拽占位符
  dragCloneBg:   { light: 'rgba(255, 255, 255, 0.95)', dark: 'rgba(50, 50, 50, 0.95)' },
  dragCloneText: { light: '#333', dark: '#e0e0e0' },
  dragCloneShadow: { light: '0 5px 15px rgba(0,0,0,0.2)', dark: '0 5px 15px rgba(0,0,0,0.5)' },

  // 错误/警告色
  errorText:     { light: '#e74c3c', dark: '#f07070' },
  successBg:     { light: 'rgba(72, 187, 120, 0.2)', dark: 'rgba(72, 187, 120, 0.15)' },
  successText:   { light: '#48bb78', dark: '#68d898' },
  dangerColor:   { light: '#f5576c', dark: '#ff7088' },

  // 看板相关
  kanbanCardText: { light: '#333', dark: '#ddd' },
  kanbanColBorder: { light: '1px solid #ddd', dark: '1px solid #555' },
  kanbanEditBorder: { light: '2px solid #667eea', dark: '2px solid #8b9cf7' },
  kanbanBg:      { light: '#fff', dark: '#333' },
};

// 获取当前主题下的颜色值
function tc(colorKey) {
  const entry = themeColors[colorKey];
  if (!entry) return '';
  return entry.light;
}

// 背景颜色解析缓存（避免重复解析 hex 颜色）
const _bgColorCache = new Map();
const _MAX_BG_CACHE = 50;

// 解析 hex 颜色为 RGB 值（带缓存）
function parseHexToRgb(hexColor) {
  if (!hexColor || typeof hexColor !== 'string') return { r: 255, g: 255, b: 255 };
  const cacheKey = hexColor;
  if (_bgColorCache.has(cacheKey)) return _bgColorCache.get(cacheKey);

  const result = {
    r: parseInt(hexColor.slice(1, 3), 16),
    g: parseInt(hexColor.slice(3, 5), 16),
    b: parseInt(hexColor.slice(5, 7), 16)
  };

  if (_bgColorCache.size >= _MAX_BG_CACHE) {
    const firstKey = _bgColorCache.keys().next().value;
    _bgColorCache.delete(firstKey);
  }
  _bgColorCache.set(cacheKey, result);
  return result;
}

// 生成 softShadow 背景样式（共享函数，适配深色模式）
function getSoftShadowStyle(bgColor, bgOpacity, isEditing, showBorder = true) {
  const rgb = parseHexToRgb(bgColor);
  return {
    background: `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${bgOpacity})`,
    backdropFilter: 'none',
    boxShadow: showBorder !== false ? tc('shadowSoft') : 'none',
    border: isEditing ? tc('borderDashed') : 'none'
  };
}

// ==================== Text 组件 ====================
const TextComponent = ({ component, comp, isEditing, baseStyle, contentContainerStyle, resizeHandles, editButtons, updateComponent, onMouseDown }) => {
  const { Markdown } = dc;
  const paddingTop = comp?.paddingTop ?? 24;
  const paddingBottom = comp?.paddingBottom ?? 24;
  const paddingLeft = comp?.paddingLeft ?? 24;
  const paddingRight = comp?.paddingRight ?? 24;
  const backgroundStyle = comp?.backgroundStyle || 'glass';
  const bgColor = comp?.bgColor || '#ffffff';
  const bgOpacity = comp?.bgOpacity ?? 0.9;

  let cardBaseStyle = baseStyle;
  if (backgroundStyle === 'softShadow') {
    cardBaseStyle = { ...baseStyle, background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`, backdropFilter: 'none', boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none', border: isEditing ? tc('borderDashed') : 'none', borderRadius: (comp?.borderRadius ?? 24) + 'px', padding: '0' };
  }

  return (
    <div style={cardBaseStyle} data-component-content="true" onMouseDown={onMouseDown}>
      {resizeHandles}{editButtons}
      <div style={{ ...contentContainerStyle, paddingTop: `${paddingTop}px`, paddingBottom: `${paddingBottom}px`, paddingLeft: `${paddingLeft}px`, paddingRight: `${paddingRight}px`, overflowY: 'hidden', overflowX: 'hidden' }}>
        {comp?.showTitle !== false && <h3 style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: '600', flexShrink: 0 }} dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '标题') }} />}
        <div style={{ fontSize: '14px', color: tc('textSecondary'), overflowY: 'auto', overflowX: 'hidden', flex: 1 }} className="markdown-card-content">
          <style>{`.markdown-card-content { white-space: pre-line !important; word-wrap: break-word !important; line-height: 1.8 !important; } .markdown-card-content * { white-space: pre-line !important; }`}</style>
          <Markdown content={comp?.content || '内容'} />
        </div>
      </div>
    </div>
  );
};

// ==================== 公共链接/命令执行函数 ====================
// 统一处理 link/command 两种模式，onNavigate 回调处理 Obsidian 内部路径跳转
const executeLinkAction = (params) => {
  const { link, linkMode, commandId, commands, onNavigate } = params;
  const mode = linkMode || 'link';
  if (mode === 'command') {
    if (commandId) commands.executeCommandById(commandId);
  } else {
    if (!link) return;
    if (link.startsWith('http://') || link.startsWith('https://')) { window.open(link, '_blank', 'noopener,noreferrer'); return; }
    if (link.startsWith('obsidian://')) { window.open(link, '_blank'); return; }
    if (onNavigate) onNavigate(link);
  }
};

// ==================== Link 组件 ====================
const LinkComponent = ({ component, comp, isEditing, baseStyle, resizeHandles, editButtons, openFile, commands, onMouseDown }) => {
  const handleClick = () => {
    if (isEditing) return;
    executeLinkAction({ link: comp?.link, linkMode: comp?.linkMode, commandId: comp?.commandId, commands, onNavigate: openFile });
  };

  return (
    <div onClick={handleClick} onMouseDown={onMouseDown} style={{ ...baseStyle, cursor: isEditing ? 'move' : 'pointer', alignItems: 'center', justifyContent: 'center', gap: '8px', flexDirection: 'column', padding: '16px', background: 'transparent', backdropFilter: 'none', boxShadow: 'none', border: isEditing ? tc('borderDashed') : 'none', minWidth: '80px', minHeight: '80px' }} data-component-content="true">
      {resizeHandles}{editButtons}
      <div dangerouslySetInnerHTML={{ __html: sanitizeSvg(comp?.iconSvg || '') }} style={{ width: '48px', height: '48px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: tc('accent'), transition: 'transform 0.2s, color 0.2s' }}
        onMouseEnter={(e) => { if (!isEditing) { e.currentTarget.style.color = tc('accentHover'); e.currentTarget.style.transform = 'scale(1.1)'; } }}
        onMouseLeave={(e) => { if (!isEditing) { e.currentTarget.style.color = tc('accent'); e.currentTarget.style.transform = 'scale(1)'; } }} />
      {comp?.showTitle && comp?.title && <div style={{ fontSize: '12px', color: tc('textPrimary'), textAlign: 'center', marginTop: '4px', fontWeight: '500' }}><span dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title) }} /></div>}
    </div>
  );
};

// ==================== Query 组件 ====================
const QueryComponent = ({ component, comp, isEditing, baseStyle, contentContainerStyle, resizeHandles, editButtons, openFile, onMouseDown }) => {
  const { useMemo } = dc;
  const backgroundStyle = comp?.backgroundStyle || 'glass';
  const bgColor = comp?.bgColor || '#ffffff';
  const bgOpacity = comp?.bgOpacity ?? 0.9;
  let queryBaseStyle = baseStyle;
  if (backgroundStyle === 'softShadow') { queryBaseStyle = { ...baseStyle, background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`, backdropFilter: 'none', boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none', border: isEditing ? tc('borderDashed') : 'none' }; }

  const queryType = comp?.queryType || 'recent';
  let queryString, needsClientFilter = false, filterInfo = {};
  if (queryType === 'recent') queryString = '@page';
  else if (queryType === 'tag') { const tagName = comp?.tagName || ''; if (tagName) { queryString = '@page'; needsClientFilter = true; filterInfo = { type: 'tag', tagName }; } else queryString = '@page and $name.contains("thisshouldnevermatch123")'; }
  else if (queryType === 'path') { const pathName = comp?.pathName || ''; if (pathName) { queryString = '@page'; needsClientFilter = true; filterInfo = { type: 'path', pathName }; } else queryString = '@page and $name.contains("thisshouldnevermatch123")'; }
  else if (queryType === 'property') { const propName = comp?.propName || ''; if (propName && propName.includes('=')) { const parts = propName.split('='); const name = parts[0]?.trim(); const value = parts[1]?.trim(); if (name && value) { queryString = '@page and exists(' + name + ')'; needsClientFilter = true; filterInfo = { type: 'prop-value', propName: name, propValue: value }; } else queryString = '@page and $name.contains("thisshouldnevermatch123")'; } else queryString = propName ? '@page and exists(' + propName + ')' : '@page and $name.contains("thisshouldnevermatch123")'; }
  else queryString = comp?.query || '@page';

  const safeQuery = (queryStr) => { if (!queryStr || typeof queryStr !== 'string' || !queryStr.includes('@')) return []; try { return dc.query(queryStr); } catch (e) { return []; } };
  const pages = safeQuery(queryString);

  const filteredPages = useMemo(() => {
    if (!needsClientFilter) return pages;
    if (filterInfo.type === 'tag') { const searchTerm = filterInfo.tagName.toLowerCase(); return pages.filter(page => { const tags = page.value('tags'); if (typeof tags === 'string') return tags.toLowerCase().replace(/#/g, '').includes(searchTerm); if (Array.isArray(tags)) return tags.some(tag => String(tag).toLowerCase().replace(/#/g, '').includes(searchTerm)); return false; }); }
    if (filterInfo.type === 'path') { const searchTerm = filterInfo.pathName.toLowerCase(); return pages.filter(page => (page.$path || '').toLowerCase().includes(searchTerm)); }
    if (filterInfo.type === 'prop-value') { const { propName, propValue } = filterInfo; const searchTerm = propValue.toLowerCase(); return pages.filter(page => { const value = page.value(propName); if (value === undefined || value === null) return false; return String(value).toLowerCase().includes(searchTerm); }); }
    return pages;
  }, [pages, needsClientFilter, filterInfo]);

  // 使用 useMemo 缓存排序结果，避免每次渲染都重新排序
  const displayPages = useMemo(() => {
    const maxItems = comp?.maxItems || 6;
    if (queryType === 'recent' || queryType === 'custom') {
      const queryOrdered = queryType === 'recent' ? [...filteredPages].sort((a, b) => (b.$mtime || 0) - (a.$mtime || 0)) : filteredPages;
      return queryOrdered.slice(0, maxItems);
    }
    const sortBy = comp?.sortBy || 'mtime-desc';
    const sorted = [...filteredPages].sort((a, b) => {
      switch (sortBy) {
        case 'name-asc': return (a.$name || '').localeCompare(b.$name || '');
        case 'name-desc': return (b.$name || '').localeCompare(a.$name || '');
        case 'ctime-asc': return (a.$ctime || 0) - (b.$ctime || 0);
        case 'ctime-desc': return (b.$ctime || 0) - (a.$ctime || 0);
        case 'mtime-asc': return (a.$mtime || 0) - (b.$mtime || 0);
        case 'mtime-desc': default: return (b.$mtime || 0) - (a.$mtime || 0);
      }
    });
    return sorted.slice(0, maxItems);
  }, [filteredPages, queryType, comp?.sortBy, comp?.maxItems]);

  return (
    <div style={queryBaseStyle} data-component-content="true" onMouseDown={onMouseDown}>
      {resizeHandles}{editButtons}
      <div style={contentContainerStyle}>
        <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', flexShrink: 0 }}>{comp?.title || '查询'}</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {displayPages.map((page, idx) => (
            <div key={idx} onClick={() => !isEditing && openFile(page.$path)} style={{ padding: '12px 16px', background: tc('cardBgLight'), borderRadius: '12px', cursor: isEditing ? 'move' : 'pointer', fontSize: '14px', transition: 'all 0.2s' }}
              onMouseEnter={(e) => { if (!isEditing) e.currentTarget.style.background = tc('cardBgMedium'); }}
              onMouseLeave={(e) => { if (!isEditing) e.currentTarget.style.background = tc('cardBgLight'); }}>
              {page.value('title') || page.$name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ==================== Personal 组件 ====================
const PersonalComponent = ({ component, comp, isEditing, baseStyle, contentContainerStyle, resizeHandles, editButtons, setViewMode, setCurrentViewingFile, setViewingPersonalComponentId, openFile, commands, vault, onMouseDown }) => {
  const getAvatarSrc = () => {
    const src = comp?.avatar || '';
    if (!src) return null;
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:') || src.startsWith('file:') || src.startsWith('blob:')) return src;
    const file = vault.getAbstractFileByPath(src);
    if (file) return vault.getResourcePath(file);
    return src;
  };
  const avatarSrc = getAvatarSrc();
  const backgroundStyle = comp?.backgroundStyle || 'glass';
  const bgColor = comp?.bgColor || '#ffffff';
  const bgOpacity = comp?.bgOpacity ?? 0.9;
  let cardBaseStyle = baseStyle;
  if (backgroundStyle === 'softShadow') { cardBaseStyle = { ...baseStyle, background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`, backdropFilter: 'none', boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none', border: isEditing ? tc('borderDashed') : 'none' }; }

  const handleMenuClick = (item) => {
    if (isEditing) return;
    executeLinkAction({ link: item.link, linkMode: item.linkMode, commandId: item.commandId, commands, onNavigate: (link) => {
      const file = vault.getAbstractFileByPath(link);
      if (file) { setViewMode(true); setCurrentViewingFile(link); setViewingPersonalComponentId(comp.id); }
      else openFile(link);
    }});
  };

  return (
    <div style={cardBaseStyle} data-component-content="true" onMouseDown={onMouseDown}>
      {resizeHandles}{editButtons}
      <div style={contentContainerStyle}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px', flexShrink: 0 }}>
          {avatarSrc ? <div style={{ width: '64px', height: '64px', borderRadius: '50%', overflow: 'hidden', boxShadow: tc('shadowCard'), flexShrink: 0 }}><img src={avatarSrc} alt="头像" style={{ width: '100%', height: '100%', objectFit: 'cover' }} /></div>
            : <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '32px', color: '#fff', flexShrink: 0 }}>👤</div>}
          <div style={{ minWidth: 0 }}>
            <div style={{ fontSize: '24px', fontWeight: '700', color: tc('nameColor'), lineHeight: '1.2' }}>{comp?.name || '你的名字'}</div>
            {comp?.tagline && <div style={{ fontSize: '14px', fontWeight: '500', color: tc('taglineColor'), marginTop: '4px' }}>{comp.tagline}</div>}
          </div>
        </div>
        {(comp?.menuItems || []).map((item, idx) => (
          <div key={idx} onClick={() => handleMenuClick(item)} style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '12px 16px', borderRadius: '16px', cursor: isEditing ? 'move' : 'pointer', transition: 'all 0.2s', color: tc('menuFontColor'), textDecoration: 'none', marginBottom: '4px' }}
            onMouseEnter={(e) => { if (!isEditing) e.currentTarget.style.background = tc('menuHoverBg'); }}
            onMouseLeave={(e) => { if (!isEditing) e.currentTarget.style.background = 'transparent'; }}>
            <span style={{ width: '24px', height: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}><dc.Icon icon={item.icon} /></span>
            <span style={{ fontSize: '14px' }}>{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ==================== Image 组件 ====================
const ImageComponent = ({ component, comp, isEditing, baseStyle, resizeHandles, editButtons, vault, onMouseDown, openFile, commands }) => {
  const { useState, useEffect, useRef } = dc;
  // 异步解析图片路径 - 参照背景图片的方法
  const [resolvedImageSrc, setResolvedImageSrc] = useState(null);
  const lastSrcRef = useRef('');

  useEffect(() => {
    const src = comp?.src || '';
    if (src === lastSrcRef.current) return;
    lastSrcRef.current = src;

    if (!src) { setResolvedImageSrc(null); return; }
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:') || src.startsWith('file:') || src.startsWith('blob:')) { setResolvedImageSrc(src); return; }

    const resolveImage = async () => {
      const file = vault.getAbstractFileByPath(src);
      if (file) { setResolvedImageSrc(vault.getResourcePath(file)); return; }
      for (let i = 0; i < 5; i++) {
        await new Promise(resolve => setTimeout(resolve, 300));
        const retryFile = vault.getAbstractFileByPath(src);
        if (retryFile) { setResolvedImageSrc(vault.getResourcePath(retryFile)); return; }
      }
      setResolvedImageSrc(src);
    };
    resolveImage();
  }, [comp?.src]);

  const imageSrc = resolvedImageSrc;
  const borderStyles = { none: { borderRadius: '0', border: 'none' }, rounded: { borderRadius: (comp?.border?.radius || 12) + 'px', border: comp?.border?.enabled ? `${comp?.border?.width || 3}px solid ${comp?.border?.color || '#ffffff'}` : 'none' }, circle: { borderRadius: '50%', border: comp?.border?.enabled ? `${comp?.border?.width || 3}px solid ${comp?.border?.color || '#ffffff'}` : 'none' }, square: { borderRadius: '0', border: comp?.border?.enabled ? `${comp?.border?.width || 3}px solid ${comp?.border?.color || '#ffffff'}` : 'none' } };
  const currentBorderStyle = borderStyles[comp?.border?.style] || borderStyles.rounded;
  const shadowStyles = { none: 'none', small: '0 2px 8px rgba(0,0,0,0.1)', medium: '0 4px 16px rgba(0,0,0,0.15)', large: '0 8px 32px rgba(0,0,0,0.2)', glow: `0 0 20px ${comp?.border?.color || tc('accentBgHover')}` };
  const getFilter = () => { const filterType = comp?.filter || 'none'; const filterVal = comp?.filterValue || 100; switch (filterType) { case 'grayscale': return `grayscale(${filterVal}%)`; case 'blur': return `blur(${filterVal / 10}px)`; case 'brightness': return `brightness(${filterVal}%)`; case 'contrast': return `contrast(${filterVal}%)`; case 'saturate': return `saturate(${filterVal}%)`; case 'sepia': return `sepia(${filterVal}%)`; case 'invert': return `invert(${filterVal}%)`; default: return 'none'; } };
  const getHoverTransform = () => { const effect = comp?.hoverEffect || 'zoom'; switch (effect) { case 'zoom': return 'scale(1.05)'; case 'lift': return 'translateY(-4px)'; case 'rotate': return 'rotate(3deg)'; default: return 'none'; } };

  // 处理图片点击事件
  const handleClick = () => {
    if (isEditing) return;
    if (!comp?.enableLink) return;
    executeLinkAction({ link: comp?.link, linkMode: comp?.linkMode, commandId: comp?.commandId, commands, onNavigate: openFile });
  };

  // 根据是否启用链接设置光标样式
  const cursorStyle = isEditing ? 'move' : (comp?.enableLink ? 'pointer' : 'default');

  return (
    <div style={{ ...baseStyle, background: 'transparent', backdropFilter: 'none', boxShadow: 'none', border: 'none', padding: '0', overflow: 'visible' }} data-component-content="true"
      onMouseDown={onMouseDown}
      onClick={handleClick}
      onMouseEnter={(e) => { if (!isEditing && comp?.hoverEffect !== 'none') { const innerContainer = e.currentTarget.querySelector('div[style*="position: relative"]'); const img = innerContainer ? innerContainer.querySelector('img') : null; if (img) { img.style.transform = getHoverTransform(); if (comp?.hoverEffect === 'lift') img.style.boxShadow = shadowStyles.large; } } }}
      onMouseLeave={(e) => { if (!isEditing) { const innerContainer = e.currentTarget.querySelector('div[style*="position: relative"]'); const img = innerContainer ? innerContainer.querySelector('img') : null; if (img) { img.style.transform = 'none'; img.style.boxShadow = shadowStyles[comp?.shadow] || shadowStyles.medium; } } }}>
      {isEditing && <div style={{ position: 'absolute', top: '-2px', left: '-2px', right: '-2px', bottom: '-2px', border: tc('borderDashed'), borderRadius: '0', pointerEvents: 'none', zIndex: 1 }} />}
      {resizeHandles}{editButtons}
      <div style={{ width: '100%', height: '100%', overflow: 'hidden', borderRadius: currentBorderStyle.borderRadius || '0', border: currentBorderStyle.border || 'none', position: 'relative' }}>
        {comp?.showTitle && comp?.title && comp?.captionPosition === 'top' && <div style={{ position: 'absolute', top: '0', left: '0', right: '0', padding: '12px 16px', background: 'linear-gradient(to bottom, rgba(0,0,0,0.5), transparent)', color: '#fff', fontSize: '14px', fontWeight: '600', zIndex: 2, flexShrink: 0 }}><span dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title) }} /></div>}
        {imageSrc ? <img src={imageSrc} style={{ width: '100%', height: '100%', objectFit: comp?.objectFit || 'cover', opacity: (comp?.opacity || 100) / 100, filter: getFilter(), transition: 'all 0.3s ease', cursor: cursorStyle, pointerEvents: isEditing ? 'none' : 'auto', display: 'block' }} onError={(e) => { e.currentTarget.style.display = 'none'; const parent = e.currentTarget.parentElement; if (parent) { const errorDiv = parent.querySelector('[data-image-error]'); if (errorDiv) errorDiv.style.display = 'flex'; } }} /> : null}
        <div data-image-error="true" style={{ display: imageSrc ? 'none' : 'flex', position: imageSrc ? 'absolute' : 'relative', top: 0, left: 0, width: '100%', height: '100%', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '12px', color: tc('textMuted'), fontSize: '13px', background: 'rgba(0,0,0,0.05)' }}><span style={{ fontSize: '48px' }}>🖼️</span><span>{comp?.src ? '图片加载失败' : '请设置图片地址'}</span></div>
        {comp?.showTitle && comp?.title && comp?.captionPosition === 'bottom' && <div style={{ position: 'absolute', bottom: '0', left: '0', right: '0', padding: '12px 16px', background: 'linear-gradient(to top, rgba(0,0,0,0.5), transparent)', color: '#fff', fontSize: '14px', fontWeight: '600', zIndex: 2, flexShrink: 0 }}><span dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title) }} /></div>}
      </div>
    </div>
  );
};

// ==================== Note 组件 ====================
const NoteComponent = ({ component, comp, isEditing, baseStyle, contentContainerStyle, resizeHandles, editButtons, updateComponent, saveConfig, tempConfig, config, onMouseDown }) => {
  const noteStyles = {
    yellow: { name: '经典黄', background: '#fff394', borderLeft: '4px solid #e6ce5a', textColor: '#222', rotation: -1.5, boxShadow: '0 10px 30px rgba(0,0,0,0.15), 0 0 10px rgba(0,0,0,0.05) inset', texture: '#fff394' },
    white: { name: '简约白', background: '#ffffff', borderLeft: '4px solid #e0e0e0', textColor: '#222', rotation: 1.5, boxShadow: '0 10px 30px rgba(0,0,0,0.15), 0 0 10px rgba(0,0,0,0.05) inset', texture: '#ffffff' },
    brown: { name: '牛皮纸', background: '#f9f1e6', borderLeft: '4px solid #d9b38c', textColor: '#222', rotation: -0.8, boxShadow: '0 10px 30px rgba(0,0,0,0.15), 0 0 10px rgba(0,0,0,0.05) inset', texture: '#f9f1e6' },
    glass: { name: '毛玻璃', background: 'rgba(255, 255, 255, 0.6)', borderLeft: '4px solid rgba(255, 255, 255, 0.7)', textColor: '#1f2937', rotation: 0, boxShadow: 'rgba(255, 255, 255, 0.25) 0px 0px 20px 0px inset, rgba(0, 0, 0, 0.05) 0px 8px 20px 0px', texture: 'rgba(255, 255, 255, 0.6)', backdropFilter: 'blur(8px)' }
  };
  const currentStyle = noteStyles[comp?.noteStyle || 'yellow'] || noteStyles.yellow;
  const isGlass = comp?.noteStyle === 'glass';
  const enableTilt = comp?.enableTilt !== false;
  const enableFold = comp?.enableFold !== false;
  const notePaddingTop = comp?.paddingTop ?? 24;
  const notePaddingBottom = comp?.paddingBottom ?? 24;
  const notePaddingLeft = comp?.paddingLeft ?? 24;
  const notePaddingRight = comp?.paddingRight ?? 24;
  const fontFamilies = { default: '"Microsoft YaHei", "PingFang SC", sans-serif', songti: '"SimSun", "宋体", serif', kaiti: '"KaiTi", "楷体", "STKaiti", serif', heiti: '"SimHei", "黑体", sans-serif', mono: '"Consolas", "Monaco", "Courier New", monospace' };
  const currentFontFamily = fontFamilies[comp?.fontFamily || 'default'] || fontFamilies.default;
  const currentFontSize = comp?.fontSize || 14;

  let noteContainerStyle;
  if (isGlass && comp?.backgroundStyle === 'softShadow') {
    const bgColor = comp?.bgColor || '#ffffff'; const bgOpacity = comp?.bgOpacity ?? 0.9;
    const bgR = parseInt(bgColor.slice(1, 3), 16);
    const bgG = parseInt(bgColor.slice(3, 5), 16);
    const bgB = parseInt(bgColor.slice(5, 7), 16);
    noteContainerStyle = { ...baseStyle, padding: notePaddingTop + "px " + notePaddingRight + "px " + notePaddingBottom + "px " + notePaddingLeft + "px", background: `rgba(${bgR}, ${bgG}, ${bgB}, ${bgOpacity})`, borderLeft: 'none', borderTop: isEditing ? tc('borderDashed') : 'none', borderRight: 'none', borderBottom: 'none', boxShadow: isEditing ? '0 10px 30px rgba(102, 126, 234, 0.3)' : 'none', transform: 'none', transition: isEditing ? 'none' : 'all 0.3s ease', borderRadius: '2px', backdropFilter: isGlass ? 'blur(8px)' : 'none' };
  } else {
    const noteBorderLeft = (comp?.noteStyle === 'white' && comp?.noteBgColor) ? (() => { const r = Math.max(0, parseInt(comp.noteBgColor.slice(1,3), 16) - 40); const g = Math.max(0, parseInt(comp.noteBgColor.slice(3,5), 16) - 40); const b = Math.max(0, parseInt(comp.noteBgColor.slice(5,7), 16) - 40); return "4px solid #" + r.toString(16).padStart(2, "0") + g.toString(16).padStart(2, "0") + b.toString(16).padStart(2, "0"); })() : currentStyle.borderLeft;
    const noteBoxShadow = (comp?.noteStyle === 'white' && comp?.noteBgColor) ? (() => { const r = Math.max(0, parseInt(comp.noteBgColor.slice(1,3), 16)); const g = Math.max(0, parseInt(comp.noteBgColor.slice(3,5), 16)); const b = Math.max(0, parseInt(comp.noteBgColor.slice(5,7), 16)); return "0 10px 30px rgba(" + r + "," + g + "," + b + ",0.15), 0 0 10px rgba(" + r + "," + g + "," + b + ",0.05) inset"; })() : currentStyle.boxShadow;
    noteContainerStyle = { ...baseStyle, padding: notePaddingTop + "px " + notePaddingRight + "px " + notePaddingBottom + "px " + notePaddingLeft + "px", background: (comp?.noteStyle === 'white' && comp?.noteBgColor) ? comp.noteBgColor : currentStyle.texture, borderLeft: 'none', borderTop: isEditing ? tc('borderDashed') : 'none', borderRight: 'none', borderBottom: 'none', boxShadow: isEditing ? '0 10px 30px rgba(102, 126, 234, 0.3)' : noteBoxShadow, transform: isEditing ? 'none' : (enableTilt ? `rotate(${currentStyle.rotation}deg)` : 'none'), transition: isEditing ? 'none' : 'all 0.3s ease', borderRadius: '2px', backdropFilter: isGlass ? currentStyle.backdropFilter : 'none' }; }

return (
    <div style={noteContainerStyle} data-component-content="true"
      onMouseDown={onMouseDown}
      onMouseEnter={(e) => { if (!isEditing && enableTilt && !isGlass) { e.currentTarget.style.transform = 'rotate(0deg)'; const bgRgb = (comp?.noteStyle === 'white' && comp?.noteBgColor) ? { r: parseInt(comp.noteBgColor.slice(1,3), 16), g: parseInt(comp.noteBgColor.slice(3,5), 16), b: parseInt(comp.noteBgColor.slice(5,7), 16) } : { r: 0, g: 0, b: 0 }; e.currentTarget.style.boxShadow = "0 15px 35px rgba(" + bgRgb.r + "," + bgRgb.g + "," + bgRgb.b + ",0.2)"; } }}
      onMouseLeave={(e) => { if (!isEditing && enableTilt && !isGlass) { e.currentTarget.style.transform = `rotate(${currentStyle.rotation}deg)`; e.currentTarget.style.boxShadow = currentStyle.boxShadow; } }}>
      {resizeHandles}{editButtons}
      <style>{"@keyframes none{} .note-scroll::-webkit-scrollbar{width:4px} .note-scroll::-webkit-scrollbar-track{background:transparent} .note-scroll::-webkit-scrollbar-thumb{background:rgba(0,0,0,0.08);border-radius:2px} .note-scroll::-webkit-scrollbar-thumb:hover{background:rgba(0,0,0,0.15)} .note-scroll { scrollbar-width: thin; scrollbar-color: rgba(0,0,0,0.08) transparent; }"}</style>
      {!isEditing && enableFold && !isGlass && <div style={{ position: 'absolute', top: 0, right: 0, width: 0, height: 0, borderStyle: 'solid', borderWidth: '0 30px 30px 0', borderColor: 'transparent rgba(0,0,0,0.06) transparent transparent', pointerEvents: 'none' }} />}
      <div className="note-scroll" style={{ ...contentContainerStyle, overflowY: 'auto', overflowX: 'hidden' }}>
        {comp?.showTitle !== false && <div style={{ margin: '0 0 12px 0', fontSize: '16px', fontWeight: '600', flexShrink: 0 }} dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '便笺') }} />}
        <div contentEditable={!isEditing} style={{ fontSize: currentFontSize + 'px', fontFamily: currentFontFamily, color: currentStyle.textColor, minHeight: '120px', outline: 'none', cursor: isEditing ? 'move' : 'text', lineHeight: '1.6' }} suppressContentEditableWarning={true}
          onInput={(e) => { if (!isEditing) updateComponent(component.id, { content: e.currentTarget.innerHTML }); }}
          onBlur={async (e) => { if (!isEditing) { const newConfig = tempConfig || config; const compIndex = newConfig.components.findIndex(c => c.id === component.id); if (compIndex !== -1) { newConfig.components[compIndex].content = e.currentTarget.innerHTML; await saveConfig(newConfig); } } }}
          dangerouslySetInnerHTML={{ __html: sanitizeNoteContent(comp?.content || '点击这里开始编辑...') }} />
      </div>
    </div>
  );
};

// ==================== Clock 组件 ====================
const ClockComponent = ({ component, comp, isEditing, baseStyle, resizeHandles, editButtons, onMouseDown }) => {
  const { useState, useEffect, useRef } = dc;
  const [timeParts, setTimeParts] = useState({ h: '00', m: '00', s: '00' });
  const [dayStr, setDayStr] = useState('');
  const [dateStr, setDateStr] = useState('');
  const [greeting, setGreeting] = useState('');
  // 初始化时从格言列表中随机取一条，避免 updateMotto 因 mottoRef 缓存跳过首次设置
  const [motto, setMotto] = useState(() => {
    const mottoes = comp?.mottoes || "凡是过往，皆为序章。\n心有山海，静而无边。";
    const list = mottoes.split('\n').filter(m => m.trim() !== '');
    return list.length > 0 ? list[Math.floor(Math.random() * list.length)] : '';
  });
  const mottoRef = useRef(comp?.mottoes);

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeParts({
        h: String(now.getHours()).padStart(2, '0'),
        m: String(now.getMinutes()).padStart(2, '0'),
        s: String(now.getSeconds()).padStart(2, '0')
      });
      setDayStr(now.toLocaleDateString('en-US', { weekday: 'long' }));
      setDateStr(now.toLocaleDateString('en-GB', { day: 'numeric', month: 'long' }));
      const hour = now.getHours();
      if (hour < 12) setGreeting("早上好，开启充满活力的一天");
      else if (hour < 18) setGreeting("下午好，继续保持专注哦");
      else setGreeting("晚上好，温故而知新");
    };

    const updateMotto = () => {
      const currentMottoes = comp?.mottoes || "凡是过往，皆为序章。\n心有山海，静而无边。";
      if (currentMottoes !== mottoRef.current) {
        mottoRef.current = currentMottoes;
        const mottoList = currentMottoes.split('\n').filter(m => m.trim() !== '');
        if (mottoList.length > 0) {
          setMotto(mottoList[Math.floor(Math.random() * mottoList.length)]);
        }
      }
    };

    updateTime();
    updateMotto();
    const timer = setInterval(() => {
      updateTime();
      updateMotto();
    }, 1000);
    return () => clearInterval(timer);
  }, [comp?.mottoes]);

  const cardBaseStyle = {
    ...baseStyle, background: 'transparent', boxShadow: 'none', border: 'none',
    backdropFilter: 'none', WebkitBackdropFilter: 'none', padding: 0, overflow: 'visible'
  };

  const animStyle =
    "@keyframes digit-tick {" +
    "  0% { opacity: 0; transform: translateY(5px); }" +
    "  100% { opacity: 1; transform: translateY(0); }" +
    "}" +
    ".single-digit { display: inline-block; width: 0.6em; text-align: center; font-variant-numeric: tabular-nums; }" +
    ".animate-active { animation: digit-tick 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards; }";

  const renderDigitGroup = (val) => val.split('').map((char, index) => (
    <span key={index + '-' + char} className="single-digit animate-active">{char}</span>
  ));

  // 各项目显示开关（默认全部显示）
  const showTime = comp?.showTime !== false;
  const showDate = comp?.showDate !== false;
  const showWeekday = comp?.showWeekday !== false;
  const showMotto = comp?.showMotto !== false;
  const showGreeting = comp?.showGreeting !== false;
  const showSeconds = (comp?.timeFormat || 'withSeconds') !== 'noSeconds';

  const timeSize = comp?.timeSize || 72;
  const timeColor = comp?.timeColor || '#ffffff';
  const defaultFont = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
  const getFont = (specific) => specific || comp?.customFont || defaultFont;
  const dateFontSize = comp?.dateFontSize || 30;
  const dateColor = comp?.dateColor || '#5eaf1c';
  const weekdayFontSizeStyle = comp?.weekdayFontSize ? comp.weekdayFontSize + 'px' : 'min(140px, 30vw)';
  const weekdayColor = comp?.weekdayColor || '#f33652';
  const weekdayFontFamily = comp?.weekdayFontFamily || '"Ruthligos", cursive';
  const mottoFontSize = comp?.mottoFontSize || 14;
  const mottoColor = comp?.mottoColor || '#ffffff';
  const greetingFontSize = comp?.greetingFontSize || 20;
  const greetingColor = comp?.greetingColor || '#ffffff';

  return (
    <div style={cardBaseStyle} data-component-content="true" onMouseDown={onMouseDown}>
      <style>{animStyle}</style>
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&family=Great+Vibes&family=Pacifico&family=Sacramento&family=Caveat:wght@400;700&family=Satisfy&display=swap" />
      {resizeHandles}
      {editButtons}

      <div style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: comp?.customFont || defaultFont,
        overflow: 'visible'
      }}>
        {/* 背景：星期 */}
        {showWeekday && (
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '100%',
            textAlign: 'center',
            color: weekdayColor,
            fontFamily: weekdayFontFamily,
            fontSize: weekdayFontSizeStyle,
            zIndex: 1,
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
            opacity: comp?.weekdayOpacity ?? 0.4
          }}>
            {dayStr}
          </div>
        )}

        {/* 内容层 */}
        <div style={{ zIndex: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', marginTop: '-10px' }}>
          {/* 时间 */}
          {showTime && (
            <div style={{
              fontSize: timeSize + 'px',
              fontWeight: 600,
              color: timeColor,
              fontFamily: getFont(comp?.timeFontFamily),
              display: 'flex',
              alignItems: 'baseline',
              lineHeight: '1.1',
              marginBottom: '5px',
              textShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}>
              <div style={{ display: 'flex' }}>{renderDigitGroup(timeParts.h)}</div>
              <span style={{ margin: '0 2px', opacity: 0.6 }}>:</span>
              <div style={{ display: 'flex' }}>{renderDigitGroup(timeParts.m)}</div>
              {showSeconds && (
                <>
                  <span style={{ margin: '0 2px', opacity: 0.6 }}>:</span>
                  <div style={{ display: 'flex' }}>{renderDigitGroup(timeParts.s)}</div>
                </>
              )}
            </div>
          )}

          {/* 日期 */}
          {showDate && (
            <div style={{
              fontSize: dateFontSize + 'px',
              fontWeight: 600,
              color: dateColor,
              fontFamily: getFont(comp?.dateFontFamily),
              marginBottom: '15px',
              textShadow: '0 2px 8px rgba(0,0,0,0.3)'
            }}>
              {dateStr}
            </div>
          )}

          {/* 格言 */}
          {showMotto && (
            <div style={{
              fontSize: mottoFontSize + 'px',
              color: mottoColor,
              fontFamily: getFont(comp?.mottoFontFamily),
              opacity: 0.7,
              fontStyle: 'italic',
              textAlign: 'center',
              maxWidth: '85%',
              lineHeight: '1.5',
              marginBottom: '12px'
            }}>
              " {motto} "
            </div>
          )}

          {/* 欢迎语 */}
          {showGreeting && (
            <div style={{
              fontSize: greetingFontSize + 'px',
              color: greetingColor,
              fontFamily: getFont(comp?.greetingFontFamily),
              opacity: 0.9,
              fontWeight: 400,
              letterSpacing: '2px',
              textShadow: '0 2px 4px rgba(0,0,0,0.3)'
            }}>
              {greeting}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

return { TextComponent, LinkComponent, QueryComponent, PersonalComponent, ImageComponent, NoteComponent, ClockComponent, executeLinkAction, sanitizeHtml, sanitizeSvg, sanitizeNoteContent, tc, isDarkMode, themeColors };
```

# SharedUI

```jsx
// ==================== 外框样式设置组件 ====================
const FrameStyleSettings = ({ comp, compId, updateComponent, prefix = '' }) => {
  const currentStyle = comp?.backgroundStyle || 'glass';
  const bgColor = comp?.bgColor || '#ffffff';
  const bgOpacity = comp?.bgOpacity ?? 0.9;
  const borderRadius = comp?.borderRadius ?? 24;

  return (
    <div style={{ marginBottom: '12px' }}>
      <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
      <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
          <input type="radio" name={`bgStyle-${prefix}${compId}`} checked={currentStyle === 'glass'} onChange={() => updateComponent(compId, { backgroundStyle: 'glass' })} style={{ cursor: 'pointer' }} />毛玻璃
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
          <input type="radio" name={`bgStyle-${prefix}${compId}`} checked={currentStyle === 'softShadow'} onChange={() => updateComponent(compId, { backgroundStyle: 'softShadow' })} style={{ cursor: 'pointer' }} />柔边阴影
        </label>
      </div>
      {currentStyle === 'softShadow' && (
        <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', marginBottom: '12px' }}>
            <div style={{ flex: '0 0 60px' }}>
              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
              <input type="color" value={bgColor} onChange={(e) => updateComponent(compId, { bgColor: e.target.value })} style={{ width: '100%', height: '36px', border: tc('borderInput'), borderRadius: '6px', cursor: 'pointer', padding: '2px' }} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景透明度: {Math.round(bgOpacity * 100)}%</label>
              <input type="range" min="0" max="100" step="5" value={Math.round(bgOpacity * 100)} onChange={(e) => updateComponent(compId, { bgOpacity: parseInt(e.target.value) / 100 })} style={{ width: '100%', cursor: 'pointer' }} />
            </div>
          </div>
          <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {borderRadius}px</label>
            <input type="range" min="0" max="48" step="4" value={borderRadius} onChange={(e) => updateComponent(compId, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
          </div>
        </div>
      )}
      {currentStyle === 'glass' && (
        <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {borderRadius}px</label>
            <input type="range" min="0" max="48" step="4" value={borderRadius} onChange={(e) => updateComponent(compId, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
          </div>
        </div>
      )}
    </div>
  );
};

// ==================== 图片路径输入框（带搜索） ====================
const ImagePathInput = ({ dc, value, onChange, placeholder = '输入图片路径或 URL' }) => {
  const { useState, useRef, useEffect } = dc;
  const { vault } = dc.app;
  const [showDropdown, setShowDropdown] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState('');
  const dropdownRef = useRef(null);

  const searchImages = (searchTerm) => {
    if (!searchTerm || searchTerm.length === 0) { setSearchResults([]); return; }
    if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) { setSearchResults([{ type: 'url', path: searchTerm }]); return; }
    const allFiles = vault.getFiles();
    const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico', '.avif'];
    const imageFiles = allFiles.filter(f => imageExtensions.some(ext => f.path.toLowerCase().endsWith(ext)));
    const matches = imageFiles.filter(f => f.path.toLowerCase().includes(searchTerm.toLowerCase())).slice(0, 10);
    setSearchResults(matches.map(f => ({ type: 'file', path: f.path })));
  };

  const handleSelect = async (path) => {
    if (path.startsWith('http://') || path.startsWith('https://')) {
      const img = new Image(); img.onload = () => { setError(''); onChange(path); }; img.onerror = () => setError('图片地址不正确'); img.src = path;
    } else { setError(''); onChange(path); }
    setShowDropdown(false);
  };

  useEffect(() => { const handleClickOutside = (e) => { if (dropdownRef.current && !dropdownRef.current.contains(e.target)) setShowDropdown(false); }; document.addEventListener('mousedown', handleClickOutside); return () => document.removeEventListener('mousedown', handleClickOutside); }, []);

  return (
    <div style={{ position: 'relative' }}>
      <input type="text" value={value || ''} placeholder={placeholder} onFocus={() => setShowDropdown(true)} onChange={(e) => { onChange(e.target.value); searchImages(e.target.value); }} style={{ width: '100%', padding: '8px 12px', border: tc('borderInput'), borderRadius: '6px', fontSize: '14px' }} />
      {error && <div style={{ color: tc('errorText'), fontSize: '11px', marginTop: '4px' }}>{error}</div>}
      {showDropdown && searchResults.length > 0 && (
        <div ref={dropdownRef} style={{ position: 'absolute', top: '100%', left: 0, right: 0, background: tc('bgInput'), border: tc('borderInput'), borderRadius: '6px', boxShadow: tc('shadowPopup'), zIndex: 100, maxHeight: '200px', overflowY: 'auto', marginTop: '4px' }}>
          {searchResults.map((item, idx) => (
            <div key={idx} onClick={() => handleSelect(item.path)} style={{ padding: '8px 12px', cursor: 'pointer', fontSize: '12px', borderBottom: idx < searchResults.length - 1 ? tc('borderSubtle') : 'none' }}
              onMouseEnter={(e) => e.currentTarget.style.background = tc('accentSubtle')}
              onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}>
              {item.type === 'url' ? '🔗 ' : '🖼️ '}{item.path}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ==================== 图片上传按钮 ====================
const ImageUploadButton = ({ dc, onUpload, currentFilePath }) => {
  const { vault, app } = dc;
  const handleUpload = async () => {
    const input = document.createElement('input'); input.type = 'file'; input.accept = 'image/*';
    input.onchange = async (e) => { const file = e.target.files?.[0]; if (!file) return; try { const timestamp = Date.now(); const ext = file.name.split('.').pop() || 'png'; const fileName = `upload_${timestamp}.${ext}`; const filePath = await app.fileManager.getAvailablePathForAttachment(fileName, currentFilePath); const arrayBuffer = await file.arrayBuffer(); await vault.createBinary(filePath, arrayBuffer); if (onUpload) onUpload(filePath); } catch (error) { console.error('上传失败:', error); } };
    input.click();
  };
  return <button onClick={handleUpload} style={{ padding: '8px 16px', background: tc('accent'), border: 'none', borderRadius: '6px', color: '#fff', fontSize: '13px', cursor: 'pointer', whiteSpace: 'nowrap' }}
    onMouseEnter={(e) => e.currentTarget.style.background = tc('accentHover')}
    onMouseLeave={(e) => e.currentTarget.style.background = tc('accent')}>📤 上传</button>;
};

return { FrameStyleSettings, ImagePathInput, ImageUploadButton };
```

# ViewComponent

```jsx
// ==================== 导入组件渲染器（必须在最顶层）==================
const { ImageComponent, NoteComponent, ClockComponent, executeLinkAction, sanitizeHtml, sanitizeSvg, sanitizeNoteContent, tc, isDarkMode, themeColors } = await dc.require(dc.headerLink(dc.resolvePath("PersonalHomepageCode.md"), "ComponentRenderers"));

const app = this.app;
const { vault, workspace, commands } = app;

// ==================== 默认配置 ====================
const DEFAULT_CONFIG = {
  background: {
    type: 'gradient',
    value: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    image: '',
    video: ''
  },
  components: []
};

// ==================== 组件类型定义 ====================
const COMPONENT_TYPES = [
  { id: 'clock', name: '时钟格言', icon: '⏰', defaultConfig: { timeSize: 72, customFont: 'Segoe UI Light', timeColor: '#ffffff', timeFontFamily: '', dateFontSize: 30, dateColor: '#5eaf1c', dateFontFamily: '', weekdayFontSize: 140, weekdayColor: '#f33652', weekdayFontFamily: '"Ruthligos", cursive', mottoFontSize: 14, mottoColor: '#ffffff', mottoFontFamily: '', greetingFontSize: 20, greetingColor: '#ffffff', greetingFontFamily: '', mottoes: "所有的伟大，都源于一个勇敢的开始。\n心有山海，静而无边。\n万物皆有裂痕，那是光照进来的地方。\n专注当下，便是胜境。\n凡是过往，皆为序章。" } },
  { id: 'text', name: 'Markdown卡片', icon: '📝', defaultConfig: { title: '标题', content: '内容描述', showTitle: true } },
  { id: 'link', name: '快捷链接', icon: '🔗', defaultConfig: { title: '', showTitle: false, linkMode: 'link', link: '', commandId: '', iconSvg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>' } },
    { id: 'query', name: '查询列表', icon: '🔍', defaultConfig: { title: '最近笔记', queryType: 'recent', query: '@page', maxItems: 6 } },
  { id: 'search', name: '搜索栏', icon: '🔎', defaultConfig: { title: '搜索', placeholder: '搜索笔记...', width: 350, height: 400, maxItems: 10 } },
  { id: 'personal', name: '主面板', icon: '👤', defaultConfig: { showPersonalInfo: true, name: '你的名字', tagline: '个性签名', avatar: '', nameFontSize: 24, nameColor: '#333f4f', nameFontFamily: '', taglineFontSize: 14, taglineColor: '#35bfab', taglineFontFamily: '', menuFontColor: '#7b888e', menuItems: [
    { label: '近期文章', icon: 'file-text', link: '', linkMode: 'link', commandId: '', openTarget: 'mini' },
    { label: '自定义项目1', icon: 'folder', link: '', linkMode: 'link', commandId: '', openTarget: 'mini' },
    { label: '自定义项目2', icon: 'smile', link: '', linkMode: 'link', commandId: '', openTarget: 'mini' },
    { label: '我的收藏', icon: 'star', link: '', linkMode: 'link', commandId: '', openTarget: 'mini' },
    { label: '自定义项目3', icon: 'globe', link: '', linkMode: 'link', commandId: '', openTarget: 'mini' }
  ]} },
  { id: 'note', name: '便笺', icon: '📌', defaultConfig: { title: '便笺', content: '点击这里开始编辑...', noteStyle: 'yellow', showTitle: false, fontFamily: 'default', fontSize: 14, enableTilt: true, enableFold: true, paddingTop: 24, paddingBottom: 24, paddingLeft: 24, paddingRight: 24, noteBgColor: '#ffffff' } },
  { id: 'kanban', name: '看板', icon: '📋', defaultConfig: {
    title: '看板',
    showBackground: true,
    columns: [
      { id: 'col1', title: '待办', cards: [{ id: 'card1', content: '任务1' }, { id: 'card2', content: '任务2' }] },
      { id: 'col2', title: '进行中', cards: [{ id: 'card3', content: '任务3' }] },
      { id: 'col3', title: '已完成', cards: [] }
    ]
  } },
  { id: 'image', name: '图片', icon: '🖼️', defaultConfig: {
    title: '',
    src: '',
    showTitle: false,
    objectFit: 'cover',
    border: {
      enabled: false,
      style: 'rounded',
      radius: 12,
      width: 3,
      color: '#ffffff'
    },
    shadow: 'medium',
    opacity: 100,
    filter: 'none',
    filterValue: 100,
    hoverEffect: 'zoom',
    captionPosition: 'bottom'
  } },
  { id: 'sidebar', name: '侧边栏视图', icon: '📑', defaultConfig: {
    title: '侧边栏',
    showTitle: false,
    showButtons: true,
    buttonsCollapsed: false,
    currentViewId: null,
    backgroundStyle: 'glass',
    bgColor: '#ffffff',
    bgOpacity: 0.9
  } },
];

// ==================== 持久化拖拽状态（跨渲染保持） ====================
const dragState = {
  offsetX: 0,
  offsetY: 0,
  kanbanDragStates: new Map(),
  dragElement: null,
  resizeElement: null,
  instanceId: null,
  // 拖拽/缩放期间的实时位置缓存，供 getBaseStyle 读取避免 React 覆盖 DOM
  dragX: 0,
  dragY: 0,
  resizeX: 0,
  resizeY: 0,
  resizeW: 0,
  resizeH: 0
};

// 获取或创建指定看板组件的拖拽状态（按组件 ID 隔离）
const getKanbanDragState = (componentId) => {
  if (!dragState.kanbanDragStates.has(componentId)) {
    dragState.kanbanDragStates.set(componentId, {
      draggingCardId: null,
      cloneElement: null,
      sourceColId: null,
      comp: null,
      isEditing: false,
      updateComponent: null
    });
  }
  return dragState.kanbanDragStates.get(componentId);
};

// ==================== 侧边栏视图组件 ====================
const SidebarView = ({ dc, app, comp, baseStyle, resizeHandles, editButtons, contentContainerStyle }) => {
  const { useState, useEffect, useRef } = dc;
  const [sidebarViews, setSidebarViews] = useState([]);
  const [currentView, setCurrentView] = useState(null);
  // 折叠状态仅作为 UI 运行时状态，不持久化，默认折叠
  const [buttonsCollapsed, setButtonsCollapsed] = useState(true);
  const embeddedSplitRef = useRef(null);
  const isMountedRef = useRef(true);
  const containerRef = useRef(null);
  const resizeObserverRef = useRef(null);
  const hasAutoLoadedRef = useRef(false);

  // ========== 切换折叠状态（纯 UI 操作，不保存到配置） ==========
  const toggleCollapse = () => {
    setButtonsCollapsed(prev => !prev);
  };

  // ========== 递归解析侧边栏视图（遍历运行时 API 对象） ==========
  const parseSidebarViews = (children, side, views) => {
    if (!children) return;
    children.forEach((child) => {
      // WorkspaceLeaf：有 view 属性
      if (child.view) {
        const viewType = child.view.getViewType ? child.view.getViewType() : null;
        if (viewType) {
          const viewState = child.getViewState ? child.getViewState() : {};
          views.push({
            id: child.id,
            type: viewType,
            title: (child.view.getDisplayText ? child.view.getDisplayText() : null) || viewType,
            icon: child.view.getIcon ? child.view.getIcon() : undefined,
            state: viewState.state || {},
            side: side
          });
        }
      } else if (child.children) {
        // WorkspaceSplit：递归遍历子节点
        parseSidebarViews(child.children, side, views);
      }
    });
  };

  // ========== 从运行时 API 获取侧边栏视图信息 ==========
  const getViewsFromWorkspace = () => {
    try {
      const views = [];

      // 解析右侧边栏
      if (app.workspace.rightSplit && app.workspace.rightSplit.children) {
        parseSidebarViews(app.workspace.rightSplit.children, "right", views);
      }

      // 解析左侧边栏
      if (app.workspace.leftSplit && app.workspace.leftSplit.children) {
        parseSidebarViews(app.workspace.leftSplit.children, "left", views);
      }

      if (isMountedRef.current) {
        setSidebarViews(views);
      }

      return views;
    } catch (err) {
      return [];
    }
  };

  // ========== 初始化视图列表 ==========
  useEffect(() => {
    let eventRef = null;

    const updateViews = () => {
      if (!isMountedRef.current) return;
      getViewsFromWorkspace();
    };

    updateViews();

    // 监听布局变化
    eventRef = app.workspace.on("layout-change", updateViews);

    // 清理函数
    return () => {
      isMountedRef.current = false;
      if (eventRef) {
        app.workspace.offref(eventRef);
      }
    };
  }, []);

  // ======== 创建独立 WorkspaceSplit ========
  const embedViewByState = async (viewInfo) => {
    if (!containerRef.current) return;

    try {
      // 显示加载状态
      containerRef.current.innerHTML = `<div style="padding: 1rem; color: var(--text-muted); text-align: center;">正在加载 ${viewInfo.title}...</div>`;

      // 清理之前的嵌入和观察者
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
        resizeObserverRef.current = null;
      }
      if (embeddedSplitRef.current) {
        try {
          embeddedSplitRef.current.detach();
        } catch (e) {
          // 忽略清理错误
        }
        embeddedSplitRef.current = null;
      }

      // 等待 DOM 更新
      await new Promise(resolve => setTimeout(resolve, 50));

      // 1. 创建独立的 WorkspaceSplit
      const WorkspaceSplit = app.workspace.rootSplit.constructor;
      const newSplit = new WorkspaceSplit(app.workspace, "vertical");

      // 2. 设置 getRoot() 返回自身，形成独立的根工作区
      newSplit.getRoot = () => newSplit;
      newSplit.getContainer = () => app.workspace.containerEl;

      // 3. 设置 split 容器的样式
      const containerHeight = containerRef.current.offsetHeight;
      newSplit.containerEl.style.width = "100%";
      newSplit.containerEl.style.height = containerHeight + "px";
      newSplit.containerEl.style.overflow = "auto";
      newSplit.containerEl.style.display = "flex";
      newSplit.containerEl.style.flexDirection = "column";

      // 4. 将 split 容器嵌入到 datacore 容器中
      containerRef.current.innerHTML = "";
      containerRef.current.appendChild(newSplit.containerEl);

      // 5. 在这个 split 中创建 leaf
      const newLeaf = app.workspace.createLeafInParent(newSplit, 0);

      // 6. 设置视图状态
      const viewState = {
        type: viewInfo.type,
        state: viewInfo.state,
        active: true
      };

      await newLeaf.setViewState(viewState);

      // 7. 等待视图初始化
      await new Promise(resolve => setTimeout(resolve, 400));

      // 8. 强制设置子元素样式，确保视图正确填充
      const children = newSplit.containerEl.children;
      for (let i = 0; i < children.length; i++) {
        const child = children[i];
        child.style.width = "100%";
        child.style.height = "100%";
        child.style.flex = "1";
        child.style.minHeight = "0";
        child.style.overflow = "auto";
      }

      // 9. 添加 ResizeObserver 监听容器高度变化
      const updateSplitHeight = () => {
        if (containerRef.current && newSplit.containerEl) {
          const newHeight = containerRef.current.offsetHeight;
          newSplit.containerEl.style.height = newHeight + "px";
        }
      };

      resizeObserverRef.current = new ResizeObserver(updateSplitHeight);
      resizeObserverRef.current.observe(containerRef.current);

      // 10. 保存 split 引用和当前视图
      embeddedSplitRef.current = newSplit;
      setCurrentView(viewInfo);

      // 保存当前视图 ID 到 localStorage（不修改笔记文件，避免触发重渲染）
      try {
        app.saveLocalStorage(`sidebar-view-${comp.id}`, viewInfo.id);
      } catch (e) {}

    } catch (err) {
      containerRef.current.innerHTML = `<div style="padding: 1rem; color: var(--text-error); text-align: center;">❌ 加载失败: ${err.message}</div>`;
    }
  };

  // ========== 自动加载保存的视图（仅执行一次） ==========
  useEffect(() => {
    // 只在视图列表加载完成且尚未自动加载过时执行
    if (sidebarViews.length === 0 || hasAutoLoadedRef.current) return;

    // 从 localStorage 读取保存的视图 ID（兼容旧配置中的 frontmatter 数据）
    let savedViewId = null;
    try { savedViewId = app.loadLocalStorage(`sidebar-view-${comp.id}`); } catch (e) {}
    if (!savedViewId) savedViewId = comp?.currentViewId;

    // 如果没有保存的视图，直接返回
    if (!savedViewId) return;

    // 查找保存的视图
    const savedView = sidebarViews.find(v => v.id === savedViewId);

    if (!savedView) return;

    // 标记已自动加载，防止 layout-change 等事件触发重载导致视图被切回
    hasAutoLoadedRef.current = true;

    // 延迟加载以确保 DOM 完全准备好
    const timer = setTimeout(() => {
      if (containerRef.current) {
        embedViewByState(savedView);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [sidebarViews]);

  // ========== 清理嵌入的 split ==========
  useEffect(() => {
    return () => {
      // 清理 ResizeObserver
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
        resizeObserverRef.current = null;
      }
      // 清理 WorkspaceSplit
      if (embeddedSplitRef.current) {
        try {
          embeddedSplitRef.current.detach();
        } catch (e) {
          // 忽略清理错误
        }
        embeddedSplitRef.current = null;
      }
    };
  }, []);

  // 按侧边栏分组
  const rightViews = sidebarViews.filter(v => v.side === "right");
  const leftViews = sidebarViews.filter(v => v.side === "left");

  // 获取背景样式
  const getBackgroundStyle = () => {
    const backgroundStyle = comp?.backgroundStyle || 'glass';
    const bgColor = comp?.bgColor || '#ffffff';
    const bgOpacity = comp?.bgOpacity ?? 0.9;

    if (backgroundStyle === 'glass') {
      return { ...baseStyle, borderRadius: (comp?.borderRadius ?? 24) + 'px' };
    } else if (backgroundStyle === 'softShadow') {
      return {
        ...baseStyle,
        background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`,
        backdropFilter: 'none',
        boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none',
        border: 'none',
        borderRadius: (comp?.borderRadius ?? 24) + 'px'
      };
    }
    return { ...baseStyle, borderRadius: (comp?.borderRadius ?? 24) + 'px' };
  };

  const cardBaseStyle = getBackgroundStyle();

  return (
    <div style={cardBaseStyle} data-component-content="true">
      {resizeHandles}
      {editButtons}
      <div style={contentContainerStyle}>
        {comp?.showTitle !== false && (
          <h3 style={{ margin: '0 0 12px 0', fontSize: '16px', fontWeight: '600', flexShrink: 0, color: '#fff' }}>
            <span dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '侧边栏') }} />
          </h3>
        )}
        <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          {/* 视图选择按钮区域 */}
          {comp?.showButtons !== false && (
            <div style={{ borderBottom: buttonsCollapsed ? 'none' : '1px solid rgba(255,255,255,0.1)', flexShrink: 0 }}>
              {/* 折叠/展开按钮 */}
              <div
                onClick={toggleCollapse}
                style={{
                  padding: '4px 8px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-start',
                  userSelect: 'none',
                  transition: 'background 0.2s',
                  minHeight: '24px'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255,255,255,0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'transparent';
                }}
              >
                <span
                  style={{
                    fontSize: '10px',
                    transition: 'transform 0.2s',
                    transform: buttonsCollapsed ? 'rotate(-90deg)' : 'rotate(0deg)',
                    cursor: 'pointer',
                    lineHeight: '1',
                    display: 'block'
                  }}
                  title={buttonsCollapsed ? '展开' : '折叠'}
                >
                  ▼
                </span>
              </div>

              {/* 可折叠的按钮列表 */}
              {!buttonsCollapsed && (
                <div style={{ padding: '12px', paddingTop: '0' }}>
                  {/* 右侧边栏视图 */}
                  {rightViews.length > 0 && (
                    <div style={{ marginBottom: leftViews.length > 0 ? '12px' : '0' }}>
                      <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.6)', marginBottom: '6px' }}>
                        右侧边栏（{rightViews.length}）
                      </div>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {rightViews.map((view) => (
                          <button
                            key={view.id}
                            onClick={() => embedViewByState(view)}
                            style={{
                              padding: '4px 10px',
                              cursor: 'pointer',
                              borderRadius: '12px',
                              border: '1px solid rgba(255,255,255,0.2)',
                              backgroundColor: currentView?.id === view.id ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.1)',
                              color: '#fff',
                              fontSize: '12px',
                              transition: 'all 0.2s',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.25)';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.backgroundColor = currentView?.id === view.id ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.1)';
                            }}
                            title={`类型: ${view.type}`}
                          >
                            📌 {view.title}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 左侧边栏视图 */}
                  {leftViews.length > 0 && (
                    <div>
                      <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.6)', marginBottom: '6px' }}>
                        左侧边栏（{leftViews.length}）
                      </div>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {leftViews.map((view) => (
                          <button
                            key={view.id}
                            onClick={() => embedViewByState(view)}
                            style={{
                              padding: '4px 10px',
                              cursor: 'pointer',
                              borderRadius: '12px',
                              border: '1px solid rgba(255,255,255,0.2)',
                              backgroundColor: currentView?.id === view.id ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.1)',
                              color: '#fff',
                              fontSize: '12px',
                              transition: 'all 0.2s',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.25)';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.backgroundColor = currentView?.id === view.id ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.1)';
                            }}
                            title={`类型: ${view.type}`}
                          >
                            📌 {view.title}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 没有视图时的提示 */}
                  {sidebarViews.length === 0 && (
                    <div style={{ color: 'rgba(255,255,255,0.5)', fontSize: '12px', textAlign: 'center' }}>
                      正在读取 workspace.json...
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* 嵌入视图容器 */}
          <div
            ref={containerRef}
            style={{
              flex: 1,
              border: comp?.showButtons !== false ? 'none' : '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              overflow: 'visible',
              backgroundColor: 'var(--background-primary)',
              position: 'relative',
              minHeight: '200px'
            }}
          />
        </div>
      </div>
    </div>
  );
};

// ==================== 主组件 ====================
function EditableHomepage() {
  const { useState, useEffect, useMemo, Markdown, useRef } = dc;
  const [isVisible, setIsVisible] = useState(true);
  // 多实例配置管理：每个文件有独立的配置
  const [configMap, setConfigMap] = useState({});
  const [currentFilePath, setCurrentFilePath] = useState(null);
  // 获取当前文件的配置
  const config = currentFilePath && configMap[currentFilePath] ? configMap[currentFilePath] : DEFAULT_CONFIG;
  // 用 ref 始终持有最新配置，避免闭包过时导致保存覆盖
  const configRef = useRef(config);
  const [isEditing, setIsEditing] = useState(false);
  const [showPageSettings, setShowPageSettings] = useState(false);
  const [menuExpanded, setMenuExpanded] = useState(false);
  const [menuPin, setMenuPin] = useState(false);
  const menuCollapseTimer = useRef(null);
  const [pageSettingsPos, setPageSettingsPos] = useState({ right: 16, top: 56 });
  const [pageSettingsWidth, setPageSettingsWidth] = useState(280);
  const [showAuxGridSettings, setShowAuxGridSettings] = useState(false);
  const [draggingSettings, setDraggingSettings] = useState(false);
  const [resizingSettings, setResizingSettings] = useState(false);
  const [editingComponent, setEditingComponent] = useState(null);
  const [draggingId, setDraggingId] = useState(null);

  // 根容器引用和实例 ID
  const rootContainerRef = useRef(null);
  // DOM 移动全屏所需的引用
  const domMoveRefs = useRef({}).current;
  // 辅助网格按钮引用
  const auxGridButtonRef = useRef(null);
  // 辅助网格 Canvas 引用
  const gridCanvasRef = useRef(null);
  // 为每个组件实例生成唯一 ID，用于区分多个打开的主页文件
  const instanceId = useRef(`homepage-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`).current;
  const [resizingId, setResizingId] = useState(null);
  const [resizeDir, setResizeDir] = useState(null);
  const [initialCompState, setInitialCompState] = useState(null);
  const [initialMousePos, setInitialMousePos] = useState(null);
  // 全局看板右键菜单状态
  const [kanbanContextMenu, setKanbanContextMenu] = useState(null);
  // search 组件状态（按组件 ID 存储多个实例的状态）
  const [searchStates, setSearchStates] = useState({});
  // kanban 组件状态（按组件 ID 存储多个实例的状态）
  const [kanbanStates, setKanbanStates] = useState({});
  // 对齐基准线状态
  const [guideLines, setGuideLines] = useState({ horizontal: [], vertical: [] });
  // 命令选择器状态（用于编辑弹窗中的命令选择）
  const [commandSelectorState, setCommandSelectorState] = useState({
    searchQuery: '',
    showList: false,
    isComposing: false,
    currentComponentId: null, // 当前正在编辑的组件ID
    isUserEditing: false // 用户是否正在编辑
  });
  // 链接输入状态（用于编辑弹窗中的链接输入）
  const [linkInputState, setLinkInputState] = useState({
    value: '',
    currentComponentId: null
  });
  // 文件查看模式状态
  const [viewMode, setViewMode] = useState(false);
  // 辅助网格配置
  const [auxGrid, setAuxGrid] = useState({
    show: false,
    lineColor: 'rgba(102, 126, 234, 0.3)',
    showHorizontal: true,
    showVertical: true,
    horizontalDensity: 50,
    verticalDensity: 50,
    lineWidth: 1
  });
  // Canvas 绘制辅助网格
  useEffect(() => {
    if (!auxGrid.show) return;
    const canvas = gridCanvasRef.current;
    if (!canvas) return;

    const drawGrid = () => {
      const parent = canvas.parentElement;
      if (!parent) return;
      const rect = parent.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';

      const ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, rect.width, rect.height);
      ctx.strokeStyle = auxGrid.lineColor;
      ctx.lineWidth = auxGrid.lineWidth;

      if (auxGrid.showHorizontal) {
        for (let y = 0; y < rect.height; y += auxGrid.horizontalDensity) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(rect.width, y);
          ctx.stroke();
        }
      }

      if (auxGrid.showVertical) {
        for (let x = 0; x < rect.width; x += auxGrid.verticalDensity) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, rect.height);
          ctx.stroke();
        }
      }
    };

    drawGrid();

    const parent = canvas.parentElement;
    if (!parent) return;
    const resizeObserver = new ResizeObserver(() => { drawGrid(); });
    resizeObserver.observe(parent);
    return () => { resizeObserver.disconnect(); };
  }, [auxGrid.show, auxGrid.showHorizontal, auxGrid.showVertical, auxGrid.horizontalDensity, auxGrid.verticalDensity, auxGrid.lineColor, auxGrid.lineWidth]);

  // 辅助网格设置菜单位置
  const [auxGridSettingsPos, setAuxGridSettingsPos] = useState({ right: 200, top: 60 });
  const [currentViewingFile, setCurrentViewingFile] = useState(null);
  const [viewingPersonalComponentId, setViewingPersonalComponentId] = useState(null);
  const [showBackgroundSettings, setShowBackgroundSettings] = useState(false);
  const [showVideoSettings, setShowVideoSettings] = useState(false);
  const [bgUrlError, setBgUrlError] = useState('');
  const [videoUrlError, setVideoUrlError] = useState('');
  const [avatarUrlErrors, setAvatarUrlErrors] = useState({});
  const [editDialogPos, setEditDialogPos] = useState({ x: 0, y: 0 });
  const [isDraggingEditDialog, setIsDraggingEditDialog] = useState(false);
  const [editDialogDragStart, setEditDialogDragStart] = useState({ x: 0, y: 0 });
  // 临时 Markdown 卡片拖拽状态（使用特殊 ID）
  const [markdownCardDragState, setMarkdownCardDragState] = useState({
    draggingId: null,
    resizingId: null,
    resizeDir: null,
    initialCompState: null,
    initialMousePos: null,
    offsetX: 0,
    offsetY: 0
  });

  // 获取或初始化组件状态的辅助函数
  const getSearchState = (componentId) => {
    if (!searchStates[componentId]) {
      return {
        searchQuery: '',
        showHelp: false,
        contentResults: [],
        selectedIndex: 0,
        isComposing: false
      };
    }
    return searchStates[componentId];
  };

  const updateSearchState = (componentId, updates) => {
    setSearchStates(prev => ({
      ...prev,
      [componentId]: { ...getSearchState(componentId), ...updates }
    }));
  };

  const getKanbanState = (componentId) => {
    if (!kanbanStates[componentId]) {
      return {
        editingCardId: null,
        editingColId: null,
        draggedCardId: null,
        hoverColId: null,
        hoverIndex: -1
      };
    }
    return kanbanStates[componentId];
  };

  const updateKanbanState = (componentId, updates) => {
    setKanbanStates(prev => ({
      ...prev,
      [componentId]: { ...getKanbanState(componentId), ...updates }
    }));
  };

  // 获取临时 Markdown 卡片设置（根据主面板组件 ID 和链接生成唯一键）
  const getMarkdownCardSettings = (personalCompId, link) => {
    const currentConfig = tempConfig || config;
    const comp = currentConfig.components.find(c => c.id === personalCompId);
    if (!comp || !comp.markdownCardSettings) {
      // 默认设置（使用像素值，与其他组件一致）
      return {
        x: window.innerWidth / 2 - 450,
        y: window.innerHeight / 2 - 350,
        width: 900,
        height: 700
      };
    }
    // 使用链接作为键来获取设置
    const linkKey = link.replace(/[\/\\:#]/g, '_');
    return comp.markdownCardSettings[linkKey] || {
      x: window.innerWidth / 2 - 450,
      y: window.innerHeight / 2 - 350,
      width: 900,
      height: 700
    };
  };

  // 更新临时 Markdown 卡片设置
  const updateMarkdownCardSettings = async (personalCompId, link, updates) => {
    const newConfig = tempConfig || config;
    const compIndex = newConfig.components.findIndex(c => c.id === personalCompId);
    if (compIndex === -1) return;

    const linkKey = link.replace(/[\/\\:#]/g, '_');
    const comp = { ...newConfig.components[compIndex] };

    // 初始化 markdownCardSettings（如果不存在）
    if (!comp.markdownCardSettings) {
      comp.markdownCardSettings = {};
    }

    // 保存设置
    comp.markdownCardSettings[linkKey] = {
      ...getMarkdownCardSettings(personalCompId, link),
      ...updates
    };

    // 创建新配置对象
    const updatedComponents = [...newConfig.components];
    updatedComponents[compIndex] = comp;
    const updatedConfig = { ...newConfig, components: updatedComponents };

    // 更新配置
    if (tempConfig) {
      setTempConfig(updatedConfig);
    } else {
      await saveConfig(updatedConfig);
    }
  };

  // 处理临时 Markdown 卡片的拖拽开始
  const handleMarkdownCardDragStart = (e, personalCompId, link) => {
    if (!isEditing) return;
    e.stopPropagation();
    e.preventDefault();

    // 获取父容器（查看模式的主内容区域）
    const container = e.currentTarget.parentElement;
    if (!container) return;

    const containerRect = container.getBoundingClientRect();
    const cardSettings = getMarkdownCardSettings(personalCompId, link);

    // 计算卡片在屏幕上的实际位置
    const cardScreenX = containerRect.left + cardSettings.x;
    const cardScreenY = containerRect.top + cardSettings.y;

    // 计算鼠标相对于卡片左上角的偏移
    const offsetX = e.clientX - cardScreenX;
    const offsetY = e.clientY - cardScreenY;

    setMarkdownCardDragState({
      draggingId: { personalCompId, link },
      resizingId: null,
      resizeDir: null,
      initialCompState: cardSettings,
      initialMousePos: { x: e.clientX, y: e.clientY },
      offsetX,
      offsetY
    });
  };

  // 处理临时 Markdown 卡片的调整大小开始
  const handleMarkdownCardResizeStart = (e, personalCompId, link, dir) => {
    if (!isEditing) return;
    e.stopPropagation();
    e.preventDefault();

    setMarkdownCardDragState({
      draggingId: null,
      resizingId: { personalCompId, link },
      resizeDir: dir,
      initialCompState: getMarkdownCardSettings(personalCompId, link),
      initialMousePos: { x: e.clientX, y: e.clientY },
      offsetX: 0,
      offsetY: 0
    });
  };

  // 处理临时 Markdown 卡片的拖拽移动
  const handleMarkdownCardDragMove = (e) => {
    if (!markdownCardDragState.draggingId || !markdownCardDragState.initialCompState) return;
    e.preventDefault();

    const { personalCompId, link } = markdownCardDragState.draggingId;

    // 获取父容器
    const container = document.querySelector('[data-markdown-card-container]') ||
      e.currentTarget?.parentElement ||
      document.querySelector('.temp-markdown-card')?.parentElement;

    if (!container) return;

    const containerRect = container.getBoundingClientRect();

    // 计算新位置：鼠标位置 - 容器位置 - 鼠标在卡片内的偏移
    const newX = e.clientX - containerRect.left - markdownCardDragState.offsetX;
    const newY = e.clientY - containerRect.top - markdownCardDragState.offsetY;

    updateMarkdownCardSettings(personalCompId, link, { x: newX, y: newY });
  };

  // 处理临时 Markdown 卡片的调整大小移动
  const handleMarkdownCardResizeMove = (e) => {
    if (!markdownCardDragState.resizingId || !markdownCardDragState.initialCompState) return;

    const { personalCompId, link } = markdownCardDragState.resizingId;

    const deltaX = e.clientX - markdownCardDragState.initialMousePos.x;
    const deltaY = e.clientY - markdownCardDragState.initialMousePos.y;

    let newWidth = markdownCardDragState.initialCompState.width;
    let newHeight = markdownCardDragState.initialCompState.height;

    if (markdownCardDragState.resizeDir.includes('right')) {
      newWidth = Math.max(400, markdownCardDragState.initialCompState.width + deltaX);
    }
    if (markdownCardDragState.resizeDir.includes('bottom')) {
      newHeight = Math.max(300, markdownCardDragState.initialCompState.height + deltaY);
    }

    updateMarkdownCardSettings(personalCompId, link, { width: newWidth, height: newHeight });
  };

  // 处理临时 Markdown 卡片的拖拽/调整结束
  const handleMarkdownCardDragEnd = () => {
    if (markdownCardDragState.draggingId || markdownCardDragState.resizingId) {
      setMarkdownCardDragState({
        draggingId: null,
        resizingId: null,
        resizeDir: null,
        initialCompState: null,
        initialMousePos: null,
        offsetX: 0,
        offsetY: 0
      });
    }
  };

  // 统一所有临时 Markdown 卡片的尺寸和位置
  const unifyMarkdownCardSizes = async () => {
    if (!viewingPersonalComponentId || !currentViewingFile) return;

    const currentConfig = tempConfig || config;
    const comp = currentConfig.components.find(c => c.id === viewingPersonalComponentId);
    if (!comp || !comp.markdownCardSettings) return;

    // 获取当前卡片设置
    const currentSettings = getMarkdownCardSettings(viewingPersonalComponentId, currentViewingFile);

    // 获取主面板组件的所有菜单项链接
    const menuItems = comp?.menuItems || [];
    const links = menuItems
      .filter(item => (item.linkMode || 'link') === 'link' && item.link)
      .map(item => item.link);

    // 为所有链接更新设置
    const newConfig = { ...currentConfig };
    const compIndex = newConfig.components.findIndex(c => c.id === viewingPersonalComponentId);
    if (compIndex === -1) return;

    const updatedComp = { ...newConfig.components[compIndex] };
    if (!updatedComp.markdownCardSettings) {
      updatedComp.markdownCardSettings = {};
    }

    // 统一所有链接的设置
    links.forEach(link => {
      const linkKey = link.replace(/[\/\\:#]/g, '_');
      updatedComp.markdownCardSettings[linkKey] = {
        x: currentSettings.x,
        y: currentSettings.y,
        width: currentSettings.width,
        height: currentSettings.height
      };
    });

    newConfig.components[compIndex] = updatedComp;

    // 更新配置
    if (tempConfig) {
      setTempConfig(newConfig);
    } else {
      await saveConfig(newConfig);
    }
  };

  // 加载配置 - 已在容器初始化 effect 中处理，此函数保留用于手动重新加载
  const loadConfig = async () => {
    try {
      const activeFile = workspace.getActiveFile();
      if (!activeFile) {
        console.warn('无法获取当前活动文件');
        return;
      }

      const filePath = activeFile.path;
      setCurrentFilePath(filePath);

      const cache = app.metadataCache.getFileCache(activeFile);
      const fileConfig = cache?.frontmatter?.homepage || DEFAULT_CONFIG;

      setConfigMap(prev => ({
        ...prev,
        [filePath]: fileConfig
      }));
    } catch (e) {
      console.error('加载配置失败', e);
    }
  };

  // 保存配置 - 保存到当前文件的 frontmatter
  const saveConfig = async (newConfig) => {
    try {
      if (!currentFilePath) {
        console.warn('当前文件路径未记录，无法保存配置');
        return;
      }

      const targetFile = vault.getAbstractFileByPath(currentFilePath);
      if (!targetFile) {
        console.warn('找不到目标文件，无法保存配置');
        return;
      }

      await app.fileManager.processFrontMatter(targetFile, (frontmatter) => {
        frontmatter.homepage = newConfig;
      });

      // 更新配置映射
      setConfigMap(prev => ({
        ...prev,
        [currentFilePath]: newConfig
      }));
    } catch (e) {
      console.error('保存配置失败', e);
    }
  };

  // 临时配置（未保存）
  const [tempConfig, setTempConfig] = useState(null);

  // 浅拷贝辅助函数（替代 JSON.parse(JSON.stringify()) 以提高性能）
  const shallowCloneConfig = (cfg) => ({
    ...cfg,
    background: cfg.background ? { ...cfg.background } : undefined,
    components: cfg.components?.map(c => ({ ...c })) || []
  });

  // 同步最新配置到 ref，确保 saveSidebarConfig 等异步回调始终读取最新值
  configRef.current = tempConfig || config;

  // 编辑弹窗更新机制：
  // - 文本输入（textarea/input text）：防抖 300ms 后刷新 tempConfig，避免频繁重渲染丢失光标
  // - 非文本控件（radio/checkbox/slider/color）：立即刷新 tempConfig（含所有 pending 文本更新），确保实时预览
  // - 弹窗关闭时 flushPendingUpdates 一次性刷新剩余 pending 更新
  const pendingUpdatesRef = useRef({});
  const debounceTimerRef = useRef(null);

  const flushPendingUpdates = () => {
    const updates = pendingUpdatesRef.current;
    const ids = Object.keys(updates);
    if (ids.length === 0) return;
    const currentCfg = tempConfig || config;
    const newConfig = {
      ...currentCfg,
      components: currentCfg.components.map(c =>
        updates[c.id] ? { ...c, ...updates[c.id] } : c
      )
    };
    pendingUpdatesRef.current = {};
    debounceTimerRef.current = null;
    setTempConfig(shallowCloneConfig(newConfig));
  };

  // 文本输入用：防抖 300ms，保护光标
  const debouncedUpdateComponent = (componentId, updates) => {
    if (!pendingUpdatesRef.current[componentId]) {
      pendingUpdatesRef.current[componentId] = {};
    }
    Object.assign(pendingUpdatesRef.current[componentId], updates);
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    debounceTimerRef.current = setTimeout(flushPendingUpdates, 300);
  };

  // 非文本控件用：立即刷新，并携带所有 pending 文本更新
  const immediateUpdateComponent = (componentId, updates) => {
    // 先将本次更新写入 pending
    if (!pendingUpdatesRef.current[componentId]) {
      pendingUpdatesRef.current[componentId] = {};
    }
    Object.assign(pendingUpdatesRef.current[componentId], updates);

    // 取消待执行的防抖
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
      debounceTimerRef.current = null;
    }

    // 将所有 pending 更新（包括文本 + 本次非文本）一次性写入 tempConfig
    const allUpdates = pendingUpdatesRef.current;
    const currentCfg = tempConfig || config;
    const newConfig = {
      ...currentCfg,
      components: currentCfg.components.map(c =>
        allUpdates[c.id] ? { ...c, ...allUpdates[c.id] } : c
      )
    };
    pendingUpdatesRef.current = {};
    setTempConfig(shallowCloneConfig(newConfig));
  };

  // DOM 辅助函数：向上查找指定 class 的祖先节点
  const findNearestAncestorWithClass = (element, className) => {
    if (!element) return null;
    let current = element.parentNode;
    while (current) {
      if (current.classList && current.classList.contains(className)) return current;
      current = current.parentNode;
    }
    return null;
  };
  // DOM 辅助函数：查找直接子节点中指定 class 的元素
  const findDirectChildByClass = (parent, className) => {
    if (!parent) return null;
    for (const child of parent.children) {
      if (child.classList && child.classList.contains(className)) return child;
    }
    return null;
  };

  // 将根容器移动到 workspace-leaf-content 以实现实时预览下也能全屏
  // 初始化：加载配置（只在挂载时运行）
  useEffect(() => {
    const container = rootContainerRef.current;
    if (!container) return;

    // 给根容器添加实例 ID 标识
    container.dataset.instanceId = instanceId;

    // 获取当前活动文件（在组件挂载时立即获取，确保每个实例获取正确的文件）
    const activeFile = workspace.getActiveFile();
    if (!activeFile) {
      console.warn('无法获取当前活动文件');
      return;
    }

    const filePath = activeFile.path;

    // 立即设置当前文件路径并加载配置
    setCurrentFilePath(filePath);
    const cache = app.metadataCache.getFileCache(activeFile);
    const fileConfig = cache?.frontmatter?.homepage || DEFAULT_CONFIG;

    // 更新配置映射
    setConfigMap(prev => ({
      ...prev,
      [filePath]: fileConfig
    }));
  }, [instanceId]);

  // DOM 移动：全屏时将容器移到 workspace-leaf-content，关闭时还原到原始位置
  // 这样 position: absolute 能在实时预览和阅读模式下都正确全屏
  // 关闭时还原，入口小卡片能在原始嵌入位置正常显示
  useEffect(() => {
    const container = rootContainerRef.current;
    if (!container || !container.parentNode) return;

    if (isVisible) {
      // 全屏模式：移到 workspace-leaf-content
      const targetPaneContent = findNearestAncestorWithClass(container, 'workspace-leaf-content');
      if (!targetPaneContent) return;

      const contentWrapper = findDirectChildByClass(targetPaneContent, 'view-content') || targetPaneContent;

      // 保存原始位置（只在首次移动时保存）
      if (!domMoveRefs.originalParent) {
        domMoveRefs.originalParent = container.parentNode;
        domMoveRefs.placeholder = document.createElement('div');
        domMoveRefs.placeholder.style.display = 'none';
        container.parentNode.insertBefore(domMoveRefs.placeholder, container);
      }

      // 确保 contentWrapper 有定位上下文
      if (!domMoveRefs.parentPositionInfo) {
        const computedPosition = window.getComputedStyle(contentWrapper).position;
        domMoveRefs.parentPositionInfo = {
          element: contentWrapper,
          originalInlinePosition: contentWrapper.style.position
        };
        if (computedPosition === 'static') {
          contentWrapper.style.position = 'relative';
        }
      }

      // 将容器移到 contentWrapper 内
      contentWrapper.appendChild(container);
    } else {
      // 入口卡片模式：还原到原始位置
      if (domMoveRefs.placeholder?.parentNode) {
        domMoveRefs.placeholder.parentNode.replaceChild(container, domMoveRefs.placeholder);
      }
    }

    return () => {
      // 组件卸载时彻底清理
      if (!domMoveRefs.originalParent) return;
      if (domMoveRefs.placeholder?.parentNode) {
        domMoveRefs.placeholder.parentNode.replaceChild(container, domMoveRefs.placeholder);
      }
      if (domMoveRefs.parentPositionInfo?.element) {
        domMoveRefs.parentPositionInfo.element.style.position = domMoveRefs.parentPositionInfo.originalInlinePosition || '';
      }
      Object.keys(domMoveRefs).forEach(key => { domMoveRefs[key] = null; });
    };
  }, [isVisible]);

  // 监听标签页切换：切回主页标签页时恢复全屏，切换到其他文件时关闭主页
  useEffect(() => {
    const handleActiveLeaf = (leaf) => {
      const container = rootContainerRef.current;
      if (!container || !currentFilePath) return;
      if (!leaf?.containerEl) return;

      // 检查切换到的 leaf 是否包含主页容器
      if (leaf.containerEl.contains(container)) {
        const file = leaf.view?.file;
        if (file && file.path === currentFilePath) {
          // 回到主页标签页，确保全屏显示
          setIsVisible(true);
        } else {
          // 切换到其他笔记，关闭主页还原 DOM
          setIsVisible(false);
          setShowAuxGridSettings(false);
          setAuxGrid(prev => ({ ...prev, show: false }));
        }
      }
    };
    const ref = workspace.on('active-leaf-change', handleActiveLeaf);
    return () => workspace.offref(ref);
  }, [currentFilePath]);

  // 监听点击外部关闭看板右键菜单
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (kanbanContextMenu) {
        const menuEl = document.querySelector('[data-context-menu="true"]');
        if (menuEl && !menuEl.contains(e.target)) {
          setKanbanContextMenu(null);
        }
      }
    };

    if (kanbanContextMenu) {
      // 延迟添加监听器，避免右键菜单打开时立即触发 click
      const timer = setTimeout(() => {
        document.addEventListener('click', handleClickOutside);
      }, 10);

      return () => {
        clearTimeout(timer);
        document.removeEventListener('click', handleClickOutside);
      };
    }
  }, [kanbanContextMenu]);

  // 页面设置面板拖动和调整大小
  const handleSettingsMouseDown = (e, type) => {
    if (type === 'drag') {
      setDraggingSettings(true);
      setInitialMousePos({ x: e.clientX, y: e.clientY });
    } else if (type === 'resize') {
      setResizingSettings(true);
      setInitialMousePos({ x: e.clientX, y: e.clientY });
    }
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (draggingSettings && initialMousePos) {
        const dx = e.clientX - initialMousePos.x;
        const dy = e.clientY - initialMousePos.y;
        setPageSettingsPos(prev => ({
          right: Math.max(0, prev.right - dx),
          top: Math.max(0, prev.top + dy)
        }));
        setInitialMousePos({ x: e.clientX, y: e.clientY });
      }
      if (resizingSettings && initialMousePos) {
        const dx = e.clientX - initialMousePos.x;
        setPageSettingsWidth(prev => Math.max(250, prev + dx));
        setInitialMousePos({ x: e.clientX, y: e.clientY });
      }
    };

    const handleMouseUp = () => {
      setDraggingSettings(false);
      setResizingSettings(false);
    };

    if (draggingSettings || resizingSettings) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [draggingSettings, resizingSettings, initialMousePos]);

  // 组件编辑弹窗拖动处理
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isDraggingEditDialog) {
        setEditDialogPos({
          x: e.clientX - editDialogDragStart.x,
          y: e.clientY - editDialogDragStart.y
        });
      }
    };

    const handleMouseUp = () => {
      setIsDraggingEditDialog(false);
    };

    if (isDraggingEditDialog) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDraggingEditDialog, editDialogDragStart]);

  // 当编辑弹窗打开或关闭时重置位置
  useEffect(() => {
    setEditDialogPos({ x: 0, y: 0 });
    // 重置命令选择器状态
    if (editingComponent) {
      const comp = (tempConfig || config).components.find(c => c.id === editingComponent);
      if (comp?.type === 'link' && comp.commandId) {
        const commandsResult = commands.listCommands();
        const allCommands = Array.isArray(commandsResult) ? commandsResult : [];
        const savedCommand = allCommands.find(c => c.id === comp.commandId);
        setCommandSelectorState({
          searchQuery: savedCommand?.name || '',
          showList: false,
          isComposing: false
        });
      } else {
        setCommandSelectorState({
          searchQuery: '',
          showList: false,
          isComposing: false
        });
      }
    }
  }, [editingComponent]);

  // 更新组件（需要在 useEffect 之前定义，因为右键菜单需要使用）
  const updateComponent = (componentId, updates, shouldSave = false) => {
    const currentCfg = tempConfig || config;
    const newConfig = {
      ...currentCfg,
      components: currentCfg.components.map(c =>
        c.id === componentId ? { ...c, ...updates } : c
      )
    };

    if (shouldSave) {
      // 先用 tempConfig 立即反映变化，避免闪烁
      setTempConfig(shallowCloneConfig(newConfig));
      // 异步保存，完成后更新 configMap 并清空 tempConfig
      saveConfig(newConfig).then(() => {
        setTempConfig(null);
      });
    } else {
      // 只更新 tempConfig
      setTempConfig(shallowCloneConfig(newConfig));
    }
    return newConfig;
  };

  // 将右键菜单渲染到 document.body
  useEffect(() => {
    if (!kanbanContextMenu) {
      // 移除现有菜单
      const existingMenu = document.getElementById('kanban-context-menu');
      if (existingMenu) {
        existingMenu.remove();
      }
      return;
    }

    // 移除现有菜单
    const existingMenu = document.getElementById('kanban-context-menu');
    if (existingMenu) {
      existingMenu.remove();
    }

    // 计算菜单位置
    const menuWidth = 180;
    const menuHeight = 400;
    let left = kanbanContextMenu.x;
    let top = kanbanContextMenu.y;

    // 如果菜单右侧超出屏幕，向左偏移
    if (left + menuWidth > window.innerWidth) {
      left = window.innerWidth - menuWidth - 10;
    }
    // 如果菜单底部超出屏幕，向上偏移
    if (top + menuHeight > window.innerHeight) {
      top = window.innerHeight - menuHeight - 10;
    }

    // 创建菜单容器
    const menuEl = document.createElement('div');
    menuEl.id = 'kanban-context-menu';
    menuEl.setAttribute('data-context-menu', 'true');
    menuEl.style.cssText =
      "position: fixed;" +
      `left: ${left}px;` +
      `top: ${top}px;` +
      `background: ${tc('bgInput')};` +
      `border: ${tc('borderInput')};` +
      "border-radius: 8px;" +
      `box-shadow: ${tc('shadowPopup')};` +
      "z-index: 999999;" +
      "min-width: 160px;" +
      "padding: 8px 0;" +
      "max-height: 400px;" +
      "overflow-y: auto;";

    menuEl.oncontextmenu = (e) => e.preventDefault();

    // 根据类型创建菜单内容
    if (kanbanContextMenu.type === 'board') {
      // 添加列按钮
      const addColumnBtn = document.createElement('div');
      addColumnBtn.textContent = '➕ 添加列';
      addColumnBtn.style.cssText = `padding: 8px 16px; cursor: pointer; font-size: 13px; color: ${tc('textPrimary')};`;
      addColumnBtn.onmouseenter = (e) => e.currentTarget.style.background = tc('bgHover');
      addColumnBtn.onmouseleave = (e) => e.currentTarget.style.background = 'transparent';
      addColumnBtn.onclick = (e) => {
        e.stopPropagation();
        // 获取看板组件
        const currentConfig = isEditing ? tempConfig : config;
        const kanbanComp = currentConfig.components.find(c => c.id === kanbanContextMenu.componentId);
        if (!kanbanComp) return;

        const newColumn = {
          id: 'col' + Date.now(),
          title: '新列',
          cards: []
        };

        if (isEditing) {
          // 编辑模式：使用 updateComponent
          updateComponent(kanbanComp.id, {
            columns: [...kanbanComp.columns, newColumn]
          });
        } else {
          // 非编辑模式：使用 saveConfig 来保存并更新状态
          const newConfig = { ...config };
          const kanbanCompIndex = newConfig.components.findIndex(c => c.id === kanbanContextMenu.componentId);
          newConfig.components[kanbanCompIndex] = {
            ...kanbanComp,
            columns: [...kanbanComp.columns, newColumn]
          };
          // 直接调用 saveConfig，不要先调用 setConfig
          saveConfig(newConfig);
        }
        setKanbanContextMenu(null);
      };
      menuEl.appendChild(addColumnBtn);

      // 切换背景按钮
      const toggleBgBtn = document.createElement('div');
      const currentConfigForToggle = tempConfig || config;
      const showBg = currentConfigForToggle.components.find(c => c.id === kanbanContextMenu.componentId)?.showBackground !== false;
      toggleBgBtn.textContent = showBg ? '🚫 隐藏背景' : '🖼️ 显示背景';
      toggleBgBtn.style.cssText = `padding: 8px 16px; cursor: pointer; font-size: 13px; color: ${tc('textPrimary')};`;
      toggleBgBtn.onmouseenter = (e) => e.currentTarget.style.background = tc('bgHover');
      toggleBgBtn.onmouseleave = (e) => e.currentTarget.style.background = 'transparent';
      toggleBgBtn.onclick = (e) => {
        e.stopPropagation();
        // 始终获取最新配置
        const latestConfig = tempConfig || config;
        const kanbanComp = latestConfig.components.find(c => c.id === kanbanContextMenu.componentId);
        if (!kanbanComp) return;

        const newShowBackground = kanbanComp.showBackground === false ? true : false;

        // 使用 updateComponent 更新，非编辑模式直接保存
        updateComponent(kanbanComp.id, { showBackground: newShowBackground }, !isEditing);
        setKanbanContextMenu(null);
      };
      menuEl.appendChild(toggleBgBtn);
    } else if (kanbanContextMenu.type === 'card') {
      // 删除卡片按钮
      const deleteCardBtn = document.createElement('div');
      deleteCardBtn.textContent = '🗑️ 删除卡片';
      deleteCardBtn.style.cssText =
        "padding: 8px 16px;" +
        "cursor: pointer;" +
        "font-size: 13px;" +
        `color: ${tc('dangerColor')};` +
        "border-bottom: 1px solid #eee;";
      deleteCardBtn.onmouseenter = (e) => e.currentTarget.style.background = tc('bgError');
      deleteCardBtn.onmouseleave = (e) => e.currentTarget.style.background = 'transparent';
      deleteCardBtn.onclick = (e) => {
        e.stopPropagation();
        // 始终获取最新配置
        const latestConfig = tempConfig || config;
        const kanbanComp = latestConfig.components.find(c => c.id === kanbanContextMenu.componentId);
        if (!kanbanComp || !kanbanContextMenu.cardId || !kanbanContextMenu.sourceColId) return;

        // 创建新的列数组
        const newColumns = kanbanComp.columns.map(col => {
          if (col.id === kanbanContextMenu.sourceColId) {
            return {
              ...col,
              cards: col.cards.filter(c => c.id !== kanbanContextMenu.cardId).map(c => ({ ...c }))
            };
          }
          return { ...col, cards: col.cards.map(c => ({ ...c })) };
        });

        // 使用 updateComponent 更新，非编辑模式直接保存
        updateComponent(kanbanComp.id, { columns: newColumns }, !isEditing);
        setKanbanContextMenu(null);
      };
      menuEl.appendChild(deleteCardBtn);

      // 颜色标题
      const colorTitle = document.createElement('div');
      colorTitle.textContent = '卡片背景颜色';
      colorTitle.style.cssText = `padding: 8px 16px; font-size: 12px; color: ${tc('textLabel')}; font-weight: 600;`;
      menuEl.appendChild(colorTitle);

      // 颜色选项
      const cardColors = [
        { name: '默认', value: 'rgba(255, 255, 255, 0.5)' },
        { name: '浅黄', value: '#fff9c4' },
        { name: '浅绿', value: '#d4edda' },
        { name: '浅蓝', value: '#d1ecf1' },
        { name: '浅粉', value: '#f8d7da' },
        { name: '浅紫', value: '#e2d9f3' },
        { name: '浅灰', value: '#f8f9fa' }
      ];

      cardColors.forEach(color => {
        const colorBtn = document.createElement('div');
        colorBtn.innerHTML =
          `<span style="width: 16px; height: 16px; border-radius: 3px; border: 1px solid #ddd; background: ${color.value}; display: inline-block; margin-right: 8px;"></span>` +
          color.name;
        colorBtn.style.cssText = 'padding: 6px 16px; cursor: pointer; font-size: 13px; display: flex; align-items: center; gap: 8px;';
        colorBtn.onmouseenter = (e) => e.currentTarget.style.background = tc('bgHover');
        colorBtn.onmouseleave = (e) => e.currentTarget.style.background = 'transparent';
        colorBtn.onclick = (e) => {
          e.stopPropagation();
          // 始终获取最新配置
          const latestConfig = tempConfig || config;
          const kanbanComp = latestConfig.components.find(c => c.id === kanbanContextMenu.componentId);
          if (!kanbanComp || !kanbanContextMenu.cardId || !kanbanContextMenu.sourceColId) return;

          // 创建新的列数组和新卡片数组
          const newColumns = kanbanComp.columns.map(col => {
            if (col.id === kanbanContextMenu.sourceColId) {
              return {
                ...col,
                cards: col.cards.map(card =>
                  card.id === kanbanContextMenu.cardId
                    ? { ...card, backgroundColor: color.value }
                    : { ...card }
                )
              };
            }
            return { ...col, cards: col.cards.map(c => ({ ...c })) };
          });

          // 使用 updateComponent 更新，非编辑模式直接保存
          updateComponent(kanbanComp.id, { columns: newColumns }, !isEditing);
          setKanbanContextMenu(null);
        };
        menuEl.appendChild(colorBtn);
      });
    } else if (kanbanContextMenu.type === 'column') {
      // 删除列按钮
      const deleteColBtn = document.createElement('div');
      deleteColBtn.textContent = '🗑️ 删除列';
      deleteColBtn.style.cssText =
      "padding: 8px 16px;" +
      "cursor: pointer;" +
      "font-size: 13px;" +
      `color: ${tc('dangerColor')};` +
      "border-bottom: 1px solid #eee;";
      deleteColBtn.onmouseenter = (e) => e.currentTarget.style.background = tc('bgError');
      deleteColBtn.onmouseleave = (e) => e.currentTarget.style.background = 'transparent';
      deleteColBtn.onclick = (e) => {
        e.stopPropagation();
        // 始终获取最新配置
        const latestConfig = tempConfig || config;
        const kanbanComp = latestConfig.components.find(c => c.id === kanbanContextMenu.componentId);
        if (!kanbanComp || !kanbanContextMenu.sourceColId) return;

        // 至少保留一列
        if (kanbanComp.columns.length <= 1) {
          setKanbanContextMenu(null);
          return;
        }

        const newColumns = kanbanComp.columns.filter(c => c.id !== kanbanContextMenu.sourceColId).map(col => ({ ...col, cards: col.cards.map(c => ({ ...c })) }));

        // 使用 updateComponent 更新，非编辑模式直接保存
        updateComponent(kanbanComp.id, { columns: newColumns }, !isEditing);
        setKanbanContextMenu(null);
      };
      menuEl.appendChild(deleteColBtn);

      // 颜色标题
      const colorTitle = document.createElement('div');
      colorTitle.textContent = '列背景颜色';
      colorTitle.style.cssText = `padding: 8px 16px; font-size: 12px; color: ${tc('textLabel')}; font-weight: 600;`;
      menuEl.appendChild(colorTitle);

      // 颜色选项
      const columnColors = [
        { name: '默认', value: 'rgba(255, 255, 255, 0.3)' },
        { name: '浅黄', value: '#fffbeb' },
        { name: '浅绿', value: '#e8f5e9' },
        { name: '浅蓝', value: '#e3f2fd' },
        { name: '浅粉', value: '#fce4ec' },
        { name: '浅紫', value: '#f3e5f5' },
        { name: '浅灰', value: '#fafafa' }
      ];

      columnColors.forEach(color => {
        const colorBtn = document.createElement('div');
        colorBtn.innerHTML =
          `<span style="width: 16px; height: 16px; border-radius: 3px; border: 1px solid #ddd; background: ${color.value}; display: inline-block; margin-right: 8px;"></span>` +
          color.name;
        colorBtn.style.cssText = 'padding: 6px 16px; cursor: pointer; font-size: 13px; display: flex; align-items: center; gap: 8px;';
        colorBtn.onmouseenter = (e) => e.currentTarget.style.background = tc('bgHover');
        colorBtn.onmouseleave = (e) => e.currentTarget.style.background = 'transparent';
        colorBtn.onclick = (e) => {
          e.stopPropagation();
          // 始终获取最新配置
          const latestConfig = tempConfig || config;
          const kanbanComp = latestConfig.components.find(c => c.id === kanbanContextMenu.componentId);
          if (!kanbanComp || !kanbanContextMenu.sourceColId) return;

          // 创建新的列数组
          const newColumns = kanbanComp.columns.map(col =>
            col.id === kanbanContextMenu.sourceColId
              ? { ...col, backgroundColor: color.value, cards: col.cards.map(c => ({ ...c })) }
              : { ...col, cards: col.cards.map(c => ({ ...c })) }
          );

          // 使用 updateComponent 更新，非编辑模式直接保存
          updateComponent(kanbanComp.id, { columns: newColumns }, !isEditing);
          setKanbanContextMenu(null);
        };
        menuEl.appendChild(colorBtn);
      });
    }

    // 添加到 document.body
    document.body.appendChild(menuEl);

    // 清理函数
    return () => {
      if (menuEl.parentNode) {
        menuEl.parentNode.removeChild(menuEl);
      }
    };
  }, [kanbanContextMenu, config, isEditing, tempConfig]);

  useEffect(() => {
    loadConfig();
  }, []);

  // 打开文件（在新标签页中打开）
  const openFile = (path) => {
    const file = vault.getAbstractFileByPath(path);
    if (file) {
      workspace.getLeaf('tab').openFile(file);
    }
  };

  // 开始编辑
  const startEditing = () => {
    const configCopy = shallowCloneConfig(config);

    // 获取容器用于计算位置
    const container = document.querySelector('[data-component-container]');
    const containerStyle = container ? window.getComputedStyle(container) : null;
    const paddingX = containerStyle ? parseFloat(containerStyle.paddingLeft) : 0;
    const paddingY = containerStyle ? parseFloat(containerStyle.paddingTop) : 0;

    // 为没有位置的组件自动分配位置（保持当前视觉位置或默认位置）
    let offsetY = 50;
    configCopy.components.forEach((comp, index) => {
      // 确保有宽度
      if (!comp.width) comp.width = 280;
      if (!comp.height) comp.height = 'auto';

      // 如果没有位置信息，分配默认位置
      if (comp.x === undefined || comp.y === undefined) {
        comp.x = 50 + (index % 3) * 310; // 每3个组件换行
        comp.y = 50 + Math.floor(index / 3) * 180;
      }
    });

    setIsEditing(true);
    setAuxGrid(prev => ({ ...prev, show: false }));
    setTempConfig(configCopy);
  };

  // 取消编辑
  const cancelEditing = () => {
    setIsEditing(false);
    setShowPageSettings(false);
    setTempConfig(null);
    setShowAuxGridSettings(false);
    setAuxGrid(prev => ({ ...prev, show: false }));
  };

  // 保存并退出编辑
  const saveAndExit = async () => {
    await saveConfig(tempConfig || config);
    setIsEditing(false);
    setShowPageSettings(false);
    setTempConfig(null);
    setShowAuxGridSettings(false);
    setAuxGrid(prev => ({ ...prev, show: false }));
  };

  // 添加组件
  const addComponent = (typeId) => {
    const componentType = COMPONENT_TYPES.find(t => t.id === typeId);
    if (!componentType) return;

    // 主面板组件只允许添加一个
    if (typeId === 'personal') {
      const currentConfig = tempConfig || config;
      if (currentConfig.components.some(c => c.type === 'personal')) return;
    }

    // 获取默认配置中的宽度（如果存在），否则使用默认值
    const defaultWidth = componentType.defaultConfig.width || 280;
    const defaultHeight = componentType.defaultConfig.height || 'auto';

    const newComponent = {
      id: Date.now().toString(),
      type: typeId,
      ...componentType.defaultConfig,
      x: 50,
      y: 50,
      width: defaultWidth,
      height: defaultHeight
    };

    const newConfig = tempConfig || config;
    // 添加到数组开头，使新组件显示在最上层
    newConfig.components.unshift(newComponent);
    setTempConfig(shallowCloneConfig(newConfig));
  };

  // 删除组件
  const deleteComponent = (componentId) => {
    const newConfig = tempConfig || config;
    newConfig.components = newConfig.components.filter(c => c.id !== componentId);
    setTempConfig(shallowCloneConfig(newConfig));
    setEditingComponent(null);
  };

  // 调整组件顺序（影响 zIndex 层级）
  const reorderComponent = (componentId, direction) => {
    const newConfig = tempConfig || config;
    const index = newConfig.components.findIndex(c => c.id === componentId);
    if (index === -1) return;

    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= newConfig.components.length) return;

    // 移动组件在数组中的位置
    const [movedComponent] = newConfig.components.splice(index, 1);
    newConfig.components.splice(newIndex, 0, movedComponent);

    setTempConfig(shallowCloneConfig(newConfig));
  };

  // 设置背景
  const setBackground = (type, value, extraOptions = {}) => {
    // 如果 tempConfig 不存在，先初始化它
    if (!tempConfig) {
      const configCopy = shallowCloneConfig(config);
      setTempConfig(configCopy);
    }

    // 使用最新的 tempConfig 或 config
    const currentConfig = tempConfig || config;
    // 创建新对象，避免直接修改
    const newConfig = {
      ...currentConfig,
      background: {
        ...currentConfig.background,
        type,
        value: type === 'gradient' || type === 'solid' ? value : (type === 'video' ? value : currentConfig.background?.value || ''),
        image: type === 'image' ? value : '',
        video: type === 'video' ? value : '',
        ...extraOptions
      }
    };
    setTempConfig(shallowCloneConfig(newConfig));
  };

  // 拖拽开始
  const handleDragStart = (e, compId) => {
    if (!isEditing) return;
    // 点击输入框等可编辑元素时不触发拖拽，保证正常聚焦
    if (
      e.target.tagName === 'INPUT' ||
      e.target.tagName === 'TEXTAREA' ||
      e.target.isContentEditable ||
      e.target.closest('[contenteditable="true"]')
    ) {
      return;
    }
    e.stopPropagation();
    e.preventDefault(); // 阻止文字选中

    // 获取容器和组件的配置信息
    const container = document.querySelector('[data-component-container]');
    const comp = (tempConfig || config).components.find(c => c.id === compId);

    if (!container || !comp) return;

    // 获取容器样式计算 padding
    const containerStyle = window.getComputedStyle(container);
    const paddingX = parseFloat(containerStyle.paddingLeft);
    const paddingY = parseFloat(containerStyle.paddingTop);

    // 计算组件在容器内的实际屏幕位置
    const componentScreenX = container.getBoundingClientRect().left + paddingX + (comp.x || 0);
    const componentScreenY = container.getBoundingClientRect().top + paddingY + (comp.y || 0);

    // 计算鼠标相对于组件左上角的偏移（保持点击时的相对位置）
    dragState.offsetX = e.clientX - componentScreenX;
    dragState.offsetY = e.clientY - componentScreenY;
    // 缓存拖拽元素的 DOM 引用（内层卡片，不是外层 wrapper）
    // wrapper 只有 position:absolute 无 left/top，内层卡片才是实际控制位置的元素
    const wrapper = document.querySelector('[data-component-id="' + compId + '"]');
    dragState.dragElement = wrapper ? wrapper.firstElementChild : null;
    dragState.instanceId = instanceId;

    // 初始化拖拽位置缓存，供 getBaseStyle 读取
    dragState.dragX = comp.x || 0;
    dragState.dragY = comp.y || 0;

    setDraggingId(compId);
  };

  // 拖拽中 - 直接操作 DOM，不触发 state 更新
  const handleDragMove = (e) => {
    if (!isEditing || !draggingId || dragState.instanceId !== instanceId) return;
    e.preventDefault(); // 阻止文字选中

    // 直接获取容器
    const container = document.querySelector('[data-component-container]');
    if (!container) return;

    // 获取容器样式计算 padding
    const containerStyle = window.getComputedStyle(container);
    const paddingX = parseFloat(containerStyle.paddingLeft);
    const paddingY = parseFloat(containerStyle.paddingTop);

    const containerRect = container.getBoundingClientRect();

    // 计算新位置：鼠标位置 - (容器位置 + padding) - 鼠标在组件内的偏移
    let x = e.clientX - containerRect.left - paddingX - dragState.offsetX;
    let y = e.clientY - containerRect.top - paddingY - dragState.offsetY;

    // 获取当前组件的尺寸
    const currentConfig = tempConfig || config;
    const currentComp = currentConfig.components.find(c => c.id === draggingId);
    const compWidth = typeof currentComp?.width === 'number' ? currentComp.width : 280;
    const compHeight = typeof currentComp?.height === 'number' ? currentComp.height : 100;

    // 对齐检测
    const SNAP_THRESHOLD = 8; // 吸附阈值（像素）
    const newGuides = { horizontal: [], vertical: [] };
    let snappedX = x;
    let snappedY = y;

    // 获取其他组件
    const otherComponents = currentConfig.components.filter(c => c.id !== draggingId);

    // 当前组件的各个边缘
    const currentLeft = x;
    const currentRight = x + compWidth;
    const currentCenterX = x + compWidth / 2;
    const currentTop = y;
    const currentBottom = y + compHeight;
    const currentCenterY = y + compHeight / 2;

    otherComponents.forEach(other => {
      const otherX = other.x || 0;
      const otherY = other.y || 0;
      const otherWidth = typeof other.width === 'number' ? other.width : 280;
      const otherHeight = typeof other.height === 'number' ? other.height : 100;

      // 其他组件的各个边缘
      const otherLeft = otherX;
      const otherRight = otherX + otherWidth;
      const otherCenterX = otherX + otherWidth / 2;
      const otherTop = otherY;
      const otherBottom = otherY + otherHeight;
      const otherCenterY = otherY + otherHeight / 2;

      // 垂直基准线检测（左边缘对齐）
      if (Math.abs(currentLeft - otherLeft) < SNAP_THRESHOLD) {
        newGuides.vertical.push(otherLeft);
        snappedX = otherLeft;
      }
      // 垂直基准线检测（右边缘对齐）
      if (Math.abs(currentRight - otherRight) < SNAP_THRESHOLD) {
        newGuides.vertical.push(otherRight);
        snappedX = otherRight - compWidth;
      }
      // 垂直基准线检测（左边缘对齐右边缘）
      if (Math.abs(currentLeft - otherRight) < SNAP_THRESHOLD) {
        newGuides.vertical.push(otherRight);
        snappedX = otherRight;
      }
      // 垂直基准线检测（右边缘对齐左边缘）
      if (Math.abs(currentRight - otherLeft) < SNAP_THRESHOLD) {
        newGuides.vertical.push(otherLeft);
        snappedX = otherLeft - compWidth;
      }
      // 垂直基准线检测（中心对齐）
      if (Math.abs(currentCenterX - otherCenterX) < SNAP_THRESHOLD) {
        newGuides.vertical.push(otherCenterX);
        snappedX = otherCenterX - compWidth / 2;
      }

      // 水平基准线检测（上边缘对齐）
      if (Math.abs(currentTop - otherTop) < SNAP_THRESHOLD) {
        newGuides.horizontal.push(otherTop);
        snappedY = otherTop;
      }
      // 水平基准线检测（下边缘对齐）
      if (Math.abs(currentBottom - otherBottom) < SNAP_THRESHOLD) {
        newGuides.horizontal.push(otherBottom);
        snappedY = otherBottom - compHeight;
      }
      // 水平基准线检测（上边缘对齐下边缘）
      if (Math.abs(currentTop - otherBottom) < SNAP_THRESHOLD) {
        newGuides.horizontal.push(otherBottom);
        snappedY = otherBottom;
      }
      // 水平基准线检测（下边缘对齐上边缘）
      if (Math.abs(currentBottom - otherTop) < SNAP_THRESHOLD) {
        newGuides.horizontal.push(otherTop);
        snappedY = otherTop - compHeight;
      }
      // 水平基准线检测（中心对齐）
      if (Math.abs(currentCenterY - otherCenterY) < SNAP_THRESHOLD) {
        newGuides.horizontal.push(otherCenterY);
        snappedY = otherCenterY - compHeight / 2;
      }
    });

    // 如果有吸附，使用吸附后的位置
    if (newGuides.vertical.length > 0 || newGuides.horizontal.length > 0) {
      x = newGuides.vertical.length > 0 ? snappedX : x;
      y = newGuides.horizontal.length > 0 ? snappedY : y;
    }

    // 直接 DOM 操作移动组件，同时缓存位置供 getBaseStyle 读取
    if (dragState.dragElement) {
      dragState.dragElement.style.left = x + 'px';
      dragState.dragElement.style.top = y + 'px';
    }
    dragState.dragX = x;
    dragState.dragY = y;

    // 直接 DOM 操作更新基准线，不触发 React 渲染
    if (!dragState.guideContainer) {
      dragState.guideContainer = container.querySelector('[data-guide-container]');
    }
    if (dragState.guideContainer) {
      // 清除旧基准线
      while (dragState.guideContainer.firstChild) {
        dragState.guideContainer.removeChild(dragState.guideContainer.firstChild);
      }
      // 绘制垂直基准线
      newGuides.vertical.forEach(pos => {
        const line = document.createElement('div');
        line.className = 'ph-guide-v';
        line.style.left = pos + 'px';
        dragState.guideContainer.appendChild(line);
      });
      // 绘制水平基准线
      newGuides.horizontal.forEach(pos => {
        const line = document.createElement('div');
        line.className = 'ph-guide-h';
        line.style.top = pos + 'px';
        dragState.guideContainer.appendChild(line);
      });
    }
  };

  // 调整大小开始
  const handleResizeStart = (e, compId, dir) => {
    if (!isEditing) return;
    e.stopPropagation();
    e.preventDefault(); // 阻止文字选中

    const comp = (tempConfig || config).components.find(c => c.id === compId);
    if (!comp) return;

    setResizingId(compId);
    setResizeDir(dir);
    // 缓存缩放元素的 DOM 引用（内层卡片，不是外层 wrapper）
    const resizeWrapper = document.querySelector('[data-component-id="' + compId + '"]');
    dragState.resizeElement = resizeWrapper ? resizeWrapper.firstElementChild : null;
    // 初始化缩放位置缓存，供 getBaseStyle 读取
    dragState.resizeX = comp.x || 0;
    dragState.resizeY = comp.y || 0;
    dragState.resizeW = comp.width || 280;
    dragState.resizeH = comp.height || 100;

    // 记录初始状态
    setInitialCompState({
      x: comp.x || 0,
      y: comp.y || 0,
      width: comp.width || 280,
      height: comp.height || 100
    });
    setInitialMousePos({
      x: e.clientX,
      y: e.clientY
    });
  };

  // 调整大小中 - 直接操作 DOM，不触发 state 更新
  const handleResizeMove = (e) => {
    if (!isEditing || !resizingId || !initialCompState || !initialMousePos || dragState.instanceId !== instanceId) return;
    e.preventDefault(); // 阻止文字选中

    // 计算从开始位置到当前位置的增量
    const deltaX = e.clientX - initialMousePos.x;
    const deltaY = e.clientY - initialMousePos.y;

    // 基于初始状态计算新值
    let newX = initialCompState.x;
    let newY = initialCompState.y;
    let newWidth = initialCompState.width;
    let newHeight = initialCompState.height;

    if (resizeDir.includes('right')) {
      newWidth = Math.max(1, initialCompState.width + deltaX);
    }
    if (resizeDir.includes('left')) {
      const proposedWidth = Math.max(1, initialCompState.width - deltaX);
      newX = initialCompState.x + (initialCompState.width - proposedWidth);
      newWidth = proposedWidth;
    }
    if (resizeDir.includes('bottom')) {
      newHeight = Math.max(1, initialCompState.height + deltaY);
    }
    if (resizeDir.includes('top')) {
      const proposedHeight = Math.max(1, initialCompState.height - deltaY);
      newY = initialCompState.y + (initialCompState.height - proposedHeight);
      newHeight = proposedHeight;
    }

    // 直接 DOM 操作缩放组件，同时缓存位置/尺寸供 getBaseStyle 读取
    if (dragState.resizeElement) {
      dragState.resizeElement.style.left = newX + 'px';
      dragState.resizeElement.style.top = newY + 'px';
      dragState.resizeElement.style.width = newWidth + 'px';
      dragState.resizeElement.style.height = newHeight + 'px';
    }
    dragState.resizeX = newX;
    dragState.resizeY = newY;
    dragState.resizeW = newWidth;
    dragState.resizeH = newHeight;
  };

  // 拖拽/调整结束 - 保存最终位置到 state
  const handleDragEnd = () => {
    // 拖拽结束：从 DOM 读取最终位置并保存
    if (draggingId && dragState.dragElement) {
      const finalX = parseFloat(dragState.dragElement.style.left) || 0;
      const finalY = parseFloat(dragState.dragElement.style.top) || 0;
      updateComponent(draggingId, { x: finalX, y: finalY });
    }
    // 缩放结束：从 DOM 读取最终尺寸并保存
    if (resizingId && dragState.resizeElement) {
      const finalX = parseFloat(dragState.resizeElement.style.left) || 0;
      const finalY = parseFloat(dragState.resizeElement.style.top) || 0;
      const finalW = parseFloat(dragState.resizeElement.style.width) || 280;
      const finalH = parseFloat(dragState.resizeElement.style.height) || 100;
      updateComponent(resizingId, { x: finalX, y: finalY, width: finalW, height: finalH });
    }

    // 清除基准线 DOM
    if (dragState.guideContainer) {
      while (dragState.guideContainer.firstChild) {
        dragState.guideContainer.removeChild(dragState.guideContainer.firstChild);
      }
    }

    // 清理所有拖拽/缩放状态
    dragState.dragElement = null;
    dragState.resizeElement = null;
    dragState.guideContainer = null;
    setDraggingId(null);
    setResizingId(null);
    setResizeDir(null);
    setInitialCompState(null);
    setInitialMousePos(null);
    // 清除基准线
    setGuideLines({ horizontal: [], vertical: [] });
  };

  // 看板拖放处理 - 从 dragState.kanbanDragStates 读取状态，在 mouseup 时统一处理
  const handleKanbanDrop = (e) => {
    dragState.kanbanDragStates.forEach((state, compId) => {
      if (!state.cloneElement) return;

      state.cloneElement.remove();
      state.cloneElement = null;

      const elementUnderMouse = document.elementFromPoint(e.clientX, e.clientY);
      const columnElement = elementUnderMouse?.closest('[data-column-id]');
      const cardElement = elementUnderMouse?.closest('[data-kanban-card]');
      const targetKanbanEl = columnElement?.closest('[data-kanban-component-id]');
      const isValidDrop = targetKanbanEl && targetKanbanEl.getAttribute('data-kanban-component-id') === String(compId);

      const cardId = state.draggingCardId;
      const sourceColId = state.sourceColId;

      const kanbanContainer = document.querySelector('[data-kanban-component-id="' + compId + '"]');
      if (kanbanContainer) {
        kanbanContainer.querySelectorAll('[data-kanban-card]').forEach(el => {
          el.style.visibility = 'visible';
        });
      }

      if (isValidDrop && columnElement && cardId && sourceColId && state.comp) {
        const targetColId = columnElement.getAttribute('data-column-id');
        const columns = state.comp.columns || [];
        const sourceCol = columns.find(c => c.id === sourceColId);
        const card = sourceCol?.cards.find(c => c.id === cardId);

        if (card) {
          const targetCardId = cardElement?.getAttribute('data-kanban-card');
          if (sourceColId !== targetColId) {
            const newColumns = columns.map(col => {
              if (col.id === sourceColId) return { ...col, cards: col.cards.filter(c => c.id !== cardId) };
              if (col.id === targetColId) return { ...col, cards: [...col.cards, card] };
              return col;
            });
            state.updateComponent(compId, { columns: newColumns }, !state.isEditing);
          } else if (targetCardId && targetCardId !== cardId) {
            const targetCol = columns.find(c => c.id === targetColId);
            if (targetCol) {
              const oldIndex = targetCol.cards.findIndex(c => c.id === cardId);
              const newIndex = targetCol.cards.findIndex(c => c.id === targetCardId);
              if (oldIndex !== -1 && newIndex !== -1 && oldIndex !== newIndex) {
                const newCards = [...targetCol.cards];
                newCards.splice(oldIndex, 1);
                newCards.splice(newIndex, 0, card);
                const newColumns = columns.map(col => {
                  if (col.id === targetColId) return { ...col, cards: newCards };
                  return col;
                });
                state.updateComponent(compId, { columns: newColumns }, !state.isEditing);
              }
            }
          }
        }
      }

      state.draggingCardId = null;
      state.sourceColId = null;
    });
  };

  // Datacore 的 <Markdown> 组件内部已使用 Obsidian 原生渲染器
  // 直接使用 dc.Markdown 即可，无需额外封装

  // 退出查看模式
  const exitViewMode = () => {
    setViewMode(false);
    setCurrentViewingFile(null);
    setViewingPersonalComponentId(null);
  };


  // ==================== 性能优化：缓存组件样式对象 ====================
  // resize handles / edit buttons 已迁移到 CSS 类（ph-rs-* / ph-eb-*）
  const componentStylesCache = (() => {
    const getContentContainerStyle = () => ({
      flex: 1,
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column'
    });

    return { getContentContainerStyle };
  })();

  // 动态样式函数：仅在 isEditing/draggingId/resizingId 变化时重建
  const dynamicStylesCache = dc.useMemo(() => {
    // padding/background/backdropFilter/boxShadow/overflow/display/flexDirection 由 [data-component-content] CSS 提供
    const getBaseStyle = (component, componentIndex, currentConfig) => {
      const isDragging = draggingId === component.id;
      const isResizing = resizingId === component.id;
      const style = {
        position: 'absolute',
        borderRadius: (component.borderRadius ?? 24) + 'px',
        border: component.type === 'note' ? 'none' : (isEditing ? tc('borderDashed') : tc('borderLight')),
        cursor: isEditing ? 'move' : 'default',
        zIndex: isEditing && (isDragging || isResizing) ? 1000 : (currentConfig.components.length - componentIndex),
        transition: isEditing ? 'none' : 'all 0.2s',
        userSelect: isEditing ? 'none' : 'auto'
      };
      // 拖拽/缩放期间从 dragState 缓存读取实时位置，避免 React 用旧 state 覆盖 DOM
      if (isDragging) {
        style.left = dragState.dragX + 'px';
        style.top = dragState.dragY + 'px';
      } else {
        style.left = (component.x || 0) + 'px';
        style.top = (component.y || 0) + 'px';
      }
      if (isResizing) {
        style.left = dragState.resizeX + 'px';
        style.top = dragState.resizeY + 'px';
        style.width = dragState.resizeW + 'px';
        style.height = dragState.resizeH + 'px';
      } else {
        style.width = (component.width || 280) + 'px';
        style.height = component.type !== 'spacer' ? (component.height || 200) + 'px' : (component.height || 20) + 'px';
      }
      return style;
    };

    const getKanbanBaseStyle = (component, baseStyle, comp) => {
      const backgroundStyle = comp?.backgroundStyle || 'glass';
      const bgColor = comp?.bgColor || '#ffffff';
      const bgOpacity = comp?.bgOpacity ?? 0.9;

      if (backgroundStyle === 'softShadow' && comp?.showBackground !== false) {
        return {
          ...baseStyle,
          width: 'auto',
          height: 'auto',
          minWidth: (component.width || 960) + 'px',
          minHeight: (component.height || 400) + 'px',
          background: "rgba(" + parseInt(bgColor.slice(1, 3), 16) + ", " + parseInt(bgColor.slice(3, 5), 16) + ", " + parseInt(bgColor.slice(5, 7), 16) + ", " + bgOpacity + ")",
          border: isEditing ? tc('borderDashed') : 'none',
          boxShadow: isEditing ? '0 10px 30px rgba(102, 126, 234, 0.3)' : comp?.showBorder !== false ? tc('shadowSoft') : 'none',
          backdropFilter: 'none'
        };
      }

      return {
        ...baseStyle,
        width: 'auto',
        height: 'auto',
        minWidth: (component.width || 960) + 'px',
        minHeight: (component.height || 400) + 'px',
        background: comp?.showBackground === false ? 'transparent' : baseStyle.background,
        border: isEditing ? tc('borderDashed') : (comp?.showBackground === false ? 'none' : baseStyle.border),
        boxShadow: comp?.showBackground === false ? 'none' : baseStyle.boxShadow,
        backdropFilter: comp?.showBackground === false ? 'none' : baseStyle.backdropFilter
      };
    };

    return { getBaseStyle, getKanbanBaseStyle };
  }, [isEditing, draggingId, resizingId]);

  // 合并静态和动态样式缓存
  const getBaseStyle = (component, componentIndex, currentConfig) =>
    dynamicStylesCache.getBaseStyle(component, componentIndex, currentConfig);
  const getKanbanBaseStyle = (component, baseStyle, comp) =>
    dynamicStylesCache.getKanbanBaseStyle(component, baseStyle, comp);

  // 切换查看文件
  const switchToViewFile = (link) => {
    // 基本输入验证：防止 XSS 注入
    if (!link || typeof link !== 'string') return;

    // 移除危险字符
    const sanitizedLink = link.replace(/[<>\"'`]/g, '');

    // 处理 Obsidian 路径（可能包含 # 用于 .base 文件的视图）
    let filePath = sanitizedLink;
    const hashIndex = sanitizedLink.indexOf('#');
    if (hashIndex !== -1) {
      filePath = sanitizedLink.substring(0, hashIndex);
    }

    const file = vault.getAbstractFileByPath(filePath);
    if (file) {
      // 传递完整的链接（包括视图部分）
      setCurrentViewingFile(sanitizedLink);
    }
  };

  // 渲染 mini 主面板
  const renderMiniNavbar = () => {
    const currentConfig = tempConfig || config;
    const comp = currentConfig.components.find(c => c.id === viewingPersonalComponentId);
    if (!comp || comp.type !== 'personal') return null;

    // 获取头像图片路径
    const getAvatarSrc = () => {
      const src = comp?.avatar || '';
      if (!src) return null;

      if (src.startsWith('http://') || src.startsWith('https://') ||
          src.startsWith('data:') || src.startsWith('file:') ||
          src.startsWith('blob:')) {
        return src;
      }

      const file = vault.getAbstractFileByPath(src);
      if (file) {
        return vault.getResourcePath(file);
      }

      return src;
    };

    const avatarSrc = getAvatarSrc();

    const menuItems = comp?.menuItems || [];
    const iconCount = menuItems.length;
    const avatarSize = 40;
    const itemGap = 8;
    const itemSize = 28;
    const paddingOuter = 12;
    const innerWidth = avatarSize + itemGap + (itemSize * iconCount) + (itemGap * (iconCount - 1)) + (paddingOuter * 2);

    return (
      <div
        style={{
          position: 'absolute',
          left: '1em',
          top: '1em',
          width: 'fit-content',
          zIndex: 10001,
          animation: 'slideInFromTopLeft 0.4s ease-out forwards',
          opacity: 0
        }}
      >
        <style>{ "@keyframes slideInFromTopLeft {" +
          "  from { opacity: 0; transform: translate(-50px, -50px); }" +
          "  to { opacity: 1; transform: translate(0, 0); }" +
          "}" }</style>
        <div style={{
          width: innerWidth + 'px',
          padding: '12px',
          background: tc('cardBgGlass'),
          border: tc('borderLight'),
          borderRadius: '64px',
          boxShadow: tc('shadowGlass'),
          backdropFilter: 'blur(4px)',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}>
          {/* 头像 */}
          <div
            onClick={exitViewMode}
            style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              boxShadow: tc('shadowCard'),
              overflow: 'hidden',
              flexShrink: 0,
              cursor: 'pointer'
            }}
          >
            {avatarSrc ? (
              <img src={avatarSrc} alt="头像" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <div style={{
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '20px',
                color: '#fff'
              }}>👤</div>
            )}
          </div>

          {/* 菜单图标 */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1 }}>
            {menuItems.map((item, idx) => {
              // 处理点击事件
              const handleClick = () => {
                executeLinkAction({ link: item.link, linkMode: item.linkMode, commandId: item.commandId, commands, onNavigate: switchToViewFile });
              };

return (
                  <div
                    key={idx}
                    onClick={handleClick}
                    title={item.label || ''}
                    style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      color: comp?.menuFontColor || '#7b888e'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = tc('cardBgGlassHover');
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'transparent';
                    }}
                  >
                    <dc.Icon icon={item.icon} />
                  </div>
                );
              })}
          </div>
        </div>
      </div>
    );
  };

  // 渲染组件
  const renderComponent = (component) => {
    const currentConfig = tempConfig || config;
    const comp = currentConfig.components.find(c => c.id === component.id);
    // 获取组件在数组中的索引，用于决定 zIndex
    const componentIndex = currentConfig.components.findIndex(c => c.id === component.id);

    // 使用缓存的样式对象
    const baseStyle = getBaseStyle(component, componentIndex, currentConfig);
    const contentContainerStyle = componentStylesCache.getContentContainerStyle();

    // 调整手柄（使用 CSS 类）
    const resizeHandles = isEditing ? (
      <>
        <div className="ph-rs-t" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleResizeStart(e, component.id, 'top'); }} />
        <div className="ph-rs-b" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleResizeStart(e, component.id, 'bottom'); }} />
        <div className="ph-rs-l" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleResizeStart(e, component.id, 'left'); }} />
        <div className="ph-rs-r" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleResizeStart(e, component.id, 'right'); }} />
        <div className="ph-rs-br" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleResizeStart(e, component.id, 'bottom-right'); }} />
      </>
    ) : null;

    // 编辑按钮（右上角）- 使用 CSS 类
    const editButtons = isEditing ? (
      <div className="ph-eb-wrap">
        <button
          className="ph-eb-btn"
          onClick={(e) => {
            e.stopPropagation();
            setEditingComponent(component.id);
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = tc('cardBgGlass');
            e.currentTarget.style.transform = 'scale(1.08)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = tc('cardBgSubtle');
            e.currentTarget.style.transform = 'scale(1)';
          }}
          title="编辑组件"
        >
          ✏️
        </button>
        <button
          className="ph-eb-btn ph-eb-del"
          onClick={(e) => {
            e.stopPropagation();
            if (confirm('确定要删除这个组件吗？')) {
              deleteComponent(component.id);
            }
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(245, 87, 108, 0.4)';
            e.currentTarget.style.borderColor = 'rgba(245, 87, 108, 0.6)';
            e.currentTarget.style.transform = 'scale(1.08)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = tc('cardBgSubtle');
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.5)';
            e.currentTarget.style.transform = 'scale(1)';
          }}
          title="删除组件"
        >
          ✕
        </button>
      </div>
    ) : null;

    switch (component.type) {
      case 'text': {
        // 获取自定义内边距，默认为 24px
        const paddingTop = comp?.paddingTop ?? 24;
        const paddingBottom = comp?.paddingBottom ?? 24;
        const paddingLeft = comp?.paddingLeft ?? 24;
        const paddingRight = comp?.paddingRight ?? 24;
        // 获取背景样式设置
        const backgroundStyle = comp?.backgroundStyle || 'glass';
        const bgColor = comp?.bgColor || '#ffffff';
        const bgOpacity = comp?.bgOpacity ?? 0.9;

        // 根据背景样式创建不同的卡片样式
        let cardBaseStyle;
        if (backgroundStyle === 'glass') {
          cardBaseStyle = baseStyle;
        } else if (backgroundStyle === 'softShadow') {
          // 柔边阴影样式
          cardBaseStyle = {
            ...baseStyle,
            background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`,
            backdropFilter: 'none',
            boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none',
            border: isEditing ? tc('borderDashed') : 'none',
            borderRadius: '12px',
            padding: '0'
          };
        } else {
          // 默认毛玻璃样式
          cardBaseStyle = baseStyle;
        }

        const cardContentStyle = {
          ...contentContainerStyle,
          paddingTop: `${paddingTop}px`,
          paddingBottom: `${paddingBottom}px`,
          paddingLeft: `${paddingLeft}px`,
          paddingRight: `${paddingRight}px`,
          overflowY: 'hidden',
          overflowX: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        };

        return (
          <div style={cardBaseStyle} data-component-content="true">
            {resizeHandles}
            {editButtons}
            <div style={cardContentStyle}>
              {comp?.showTitle !== false && (
                <h3
                  style={{ margin: '0 0 12px 0', fontSize: '18px', fontWeight: '600', flexShrink: 0 }}
                  dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '标题') }}
                />
              )}
              <div style={{ fontSize: '14px', color: tc('textSecondary'), overflowY: 'auto', overflowX: 'hidden', flex: 1 }} className="markdown-card-content">
                <style>{ ".markdown-card-content {" +
                  "  white-space: pre-line !important;" +
                  "  word-wrap: break-word !important;" +
                  "  line-height: 1.8 !important;" +
                  "}" +
                  ".markdown-card-content * {" +
                  "  white-space: pre-line !important;" +
                  "}" }</style>
                <Markdown content={comp?.content || '内容'} />
              </div>
            </div>
          </div>
        );
      }

      case 'link': {
        // 处理点击事件
        const handleClick = () => {
          if (isEditing) return;
          executeLinkAction({ link: comp?.link, linkMode: comp?.linkMode, commandId: comp?.commandId, commands, onNavigate: openFile });
        };

        return (
          <div
            onClick={handleClick}
            style={{
              ...baseStyle,
              cursor: isEditing ? 'move' : 'pointer',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              flexDirection: 'column',
              padding: '16px',
              background: 'transparent',
              backdropFilter: 'none',
              boxShadow: 'none',
              border: isEditing ? tc('borderDashed') : 'none',
              minWidth: '80px',
              minHeight: '80px'
            }}
            data-component-content="true"
          >
            {resizeHandles}
            {editButtons}
            {/* 图标 */}
            <div
              dangerouslySetInnerHTML={{ __html: sanitizeSvg(comp?.iconSvg || '') }}
              style={{
                width: '48px',
                height: '48px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: tc('accent'),
                transition: 'transform 0.2s, color 0.2s'
              }}
              onMouseEnter={(e) => {
                if (!isEditing) {
                  e.currentTarget.style.color = '#5568d3';
                  e.currentTarget.style.transform = 'scale(1.1)';
                }
              }}
              onMouseLeave={(e) => {
                if (!isEditing) {
                  e.currentTarget.style.color = '#667eea';
                  e.currentTarget.style.transform = 'scale(1)';
                }
              }}
            />
            {/* 标题（可选显示） */}
            {comp?.showTitle && comp?.title && (
              <div style={{
                fontSize: '12px',
                color: tc('textPrimary'),
                textAlign: 'center',
                marginTop: '4px',
                fontWeight: '500'
              }}>
                <span dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title) }} />
              </div>
            )}
          </div>
        );
      }

      case 'query': {
        // 获取外框样式设置
        const backgroundStyle = comp?.backgroundStyle || 'glass';
        const bgColor = comp?.bgColor || '#ffffff';
        const bgOpacity = comp?.bgOpacity ?? 0.9;

        // 根据背景样式创建不同的组件样式
        let queryBaseStyle;
        if (backgroundStyle === 'glass') {
          queryBaseStyle = baseStyle;
        } else if (backgroundStyle === 'softShadow') {
          // 柔边阴影样式
          queryBaseStyle = {
            ...baseStyle,
            background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`,
            backdropFilter: 'none',
            boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none',
            border: isEditing ? tc('borderDashed') : 'none'
          };
        } else {
          queryBaseStyle = baseStyle;
        }

        // 根据查询类型构建查询语句
        const queryType = comp?.queryType || 'recent';
        let queryString;
        let needsClientFilter = false;
        let filterInfo = {};

        if (queryType === 'recent') {
          queryString = '@page';
        } else if (queryType === 'tag') {
          const tagName = comp?.tagName || '';
          if (tagName) {
            // 标签模糊匹配：查询所有页面，然后在 JavaScript 中过滤
            queryString = '@page';
            needsClientFilter = true;
            filterInfo = { type: 'tag', tagName };
          } else {
            queryString = '@page and $name.contains("thisshouldnevermatch123")';
          }
        } else if (queryType === 'path') {
          const pathName = comp?.pathName || '';
          if (pathName) {
            // 路径模糊匹配：查询所有页面，然后在 JavaScript 中过滤
            queryString = '@page';
            needsClientFilter = true;
            filterInfo = { type: 'path', pathName };
          } else {
            queryString = '@page and $name.contains("thisshouldnevermatch123")';
          }
        } else if (queryType === 'property') {
          const propName = comp?.propName || '';
          if (propName && propName.includes('=')) {
            const parts = propName.split('=');
            const name = parts[0] ? parts[0].trim() : '';
            const value = parts[1] ? parts[1].trim() : '';
            if (name && value) {
              // 属性值模糊匹配：查询有该属性的页面，然后在 JavaScript 中过滤
              queryString = '@page and exists(' + name + ')';
              needsClientFilter = true;
              filterInfo = { type: 'prop-value', propName: name, propValue: value };
            } else {
              queryString = '@page and $name.contains("thisshouldnevermatch123")';
            }
          } else {
            queryString = propName ? '@page and exists(' + propName + ')' : '@page and $name.contains("thisshouldnevermatch123")';
          }
        } else if (queryType === 'custom') {
          queryString = comp?.query || '@page';
        } else {
          queryString = comp?.query || '@page';
        }

        const safeQuery = (queryStr) => {
          if (!queryStr || typeof queryStr !== 'string' || !queryStr.includes('@')) {
            return [];
          }
          try {
            return dc.query(queryStr);
          } catch (e) {
            console.error('查询失败:', e);
            return [];
          }
        };

        const pages = safeQuery(queryString);

        // 使用 useMemo 进行客户端模糊过滤
        const filteredPages = useMemo(() => {
          if (!needsClientFilter) return pages;

          // 标签模糊匹配
          if (filterInfo.type === 'tag') {
            const searchTerm = filterInfo.tagName.toLowerCase();
            return pages.filter(page => {
              const tags = page.value('tags');
              // 处理字符串格式
              if (typeof tags === 'string') {
                return tags.toLowerCase().replace(/#/g, '').includes(searchTerm);
              }
              // 处理数组格式
              if (Array.isArray(tags)) {
                return tags.some(tag => {
                  const tagStr = String(tag).toLowerCase().replace(/#/g, '');
                  return tagStr.includes(searchTerm);
                });
              }
              return false;
            });
          }

          // 路径模糊匹配
          if (filterInfo.type === 'path') {
            const searchTerm = filterInfo.pathName.toLowerCase();
            return pages.filter(page => {
              const path = page.$path || '';
              return path.toLowerCase().includes(searchTerm);
            });
          }

          // 属性值模糊匹配
          if (filterInfo.type === 'prop-value') {
            const { propName, propValue } = filterInfo;
            const searchTerm = propValue.toLowerCase();
            return pages.filter(page => {
              const value = page.value(propName);
              if (value === undefined || value === null) return false;
              return String(value).toLowerCase().includes(searchTerm);
            });
          }

          return pages;
        }, [pages, needsClientFilter, filterInfo]);

        // 排序与截取：最近笔记/自定义查询用原逻辑，其他查询先排序再截取
        let displayPages;
        if (queryType === 'recent' || queryType === 'custom') {
          const queryOrdered = queryType === 'recent' ? [...filteredPages].sort((a, b) => (b.$mtime || 0) - (a.$mtime || 0)) : filteredPages;
          displayPages = queryOrdered.slice(0, comp?.maxItems || 6);
        } else {
          const sortBy = comp?.sortBy || 'mtime-desc';
          const sorted = [...filteredPages].sort((a, b) => {
            switch (sortBy) {
              case 'name-asc': return (a.$name || '').localeCompare(b.$name || '');
              case 'name-desc': return (b.$name || '').localeCompare(a.$name || '');
              case 'ctime-asc': return (a.$ctime || 0) - (b.$ctime || 0);
              case 'ctime-desc': return (b.$ctime || 0) - (a.$ctime || 0);
              case 'mtime-asc': return (a.$mtime || 0) - (b.$mtime || 0);
              case 'mtime-desc': default: return (b.$mtime || 0) - (a.$mtime || 0);
            }
          });
          displayPages = sorted.slice(0, comp?.maxItems || 6);
        }
        return (
          <div style={queryBaseStyle} data-component-content="true">
            {resizeHandles}
            {editButtons}
            <div style={contentContainerStyle}>
<h3 style={{ margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', flexShrink: 0 }}><span dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '查询') }} /></h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', flex: '1 1 0', minHeight: 0, overflowY: 'auto' }}>
                {displayPages.map((page, idx) => (
                  <div
                    key={idx}
                    onClick={() => !isEditing && openFile(page.$path)}
                    style={{
                      padding: '12px 16px',
                      background: tc('cardBgLight'),
                      borderRadius: '12px',
                      cursor: isEditing ? 'move' : 'pointer',
                      fontSize: '14px',
                      transition: 'all 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      if (!isEditing) e.currentTarget.style.background = tc('cardBgMedium');
                    }}
                    onMouseLeave={(e) => {
                      if (!isEditing) e.currentTarget.style.background = tc('cardBgLight');
                    }}
                  >
                    {page.value('title') || page.$name}
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      }

      case 'clock': {
        return (
          <ClockComponent
            key={component.id}
            component={component}
            comp={comp}
            isEditing={isEditing}
            baseStyle={baseStyle}
            resizeHandles={resizeHandles}
            editButtons={editButtons}
          />
        );
      }

      case 'note': {
        // 便笺样式定义（质感便笺）
        const noteStyles = {
          yellow: {
            name: '经典黄',
            background: '#fff394',
            borderLeft: '4px solid #e6ce5a',
            textColor: '#222',
            rotation: -1.5,
            boxShadow: '0 10px 30px rgba(0,0,0,0.15), 0 0 10px rgba(0,0,0,0.05) inset',
            texture: '#fff394'
          },
          white: {
            name: '简约白',
            background: '#ffffff',
            borderLeft: '4px solid #e0e0e0',
            textColor: '#222',
            rotation: 1.5,
            boxShadow: '0 10px 30px rgba(0,0,0,0.15), 0 0 10px rgba(0,0,0,0.05) inset',
            texture: '#ffffff'
          },
          brown: {
            name: '牛皮纸',
            background: '#f9f1e6',
            borderLeft: '4px solid #d9b38c',
            textColor: '#222',
            rotation: -0.8,
            boxShadow: '0 10px 30px rgba(0,0,0,0.15), 0 0 10px rgba(0,0,0,0.05) inset',
            texture: '#f9f1e6'
          },
          glass: {
            name: '毛玻璃',
            background: 'rgba(255, 255, 255, 0.6)',
            borderLeft: '4px solid rgba(255, 255, 255, 0.7)',
            textColor: '#1f2937',
            rotation: 0,
            boxShadow: 'rgba(255, 255, 255, 0.25) 0px 0px 20px 0px inset, rgba(0, 0, 0, 0.05) 0px 8px 20px 0px',
            texture: 'rgba(255, 255, 255, 0.6)',
            backdropFilter: 'blur(8px)'
          }
        };

        const currentStyle = noteStyles[comp?.noteStyle || 'yellow'] || noteStyles.yellow;
        const isGlass = comp?.noteStyle === 'glass';
        const enableTilt = comp?.enableTilt !== false;
        const enableFold = comp?.enableFold !== false;
        const notePaddingTop = comp?.paddingTop ?? 24;
        const notePaddingBottom = comp?.paddingBottom ?? 24;
        const notePaddingLeft = comp?.paddingLeft ?? 24;
        const notePaddingRight = comp?.paddingRight ?? 24;

        // 获取外框样式设置（仅毛玻璃样式时生效）
        const backgroundStyle = comp?.backgroundStyle || 'glass';
        const bgColor = comp?.bgColor || '#ffffff';
        const bgOpacity = comp?.bgOpacity ?? 0.9;

        // 字体设置
        const fontFamilies = {
          default: '"Microsoft YaHei", "PingFang SC", sans-serif',
          songti: '"SimSun", "宋体", serif',
          kaiti: '"KaiTi", "楷体", "STKaiti", serif',
          heiti: '"SimHei", "黑体", sans-serif',
          mono: '"Consolas", "Monaco", "Courier New", monospace'
        };
        const currentFontFamily = fontFamilies[comp?.fontFamily || 'default'] || fontFamilies.default;
        const currentFontSize = comp?.fontSize || 14;

        // 根据便笺样式调整容器样式
        let noteContainerStyle;
        if (isGlass && backgroundStyle === 'softShadow') {
          // 毛玻璃 + 柔边阴影 - 无外部阴影
          const bgR = parseInt(bgColor.slice(1, 3), 16);
          const bgG = parseInt(bgColor.slice(3, 5), 16);
          const bgB = parseInt(bgColor.slice(5, 7), 16);
          noteContainerStyle = {
            ...baseStyle,
            padding: notePaddingTop + "px " + notePaddingRight + "px " + notePaddingBottom + "px " + notePaddingLeft + "px",
            background: `rgba(${bgR}, ${bgG}, ${bgB}, ${bgOpacity})`,
            borderLeft: 'none',
            borderTop: isEditing ? tc('borderDashed') : 'none',
            borderRight: 'none',
            borderBottom: 'none',
            boxShadow: isEditing ? '0 10px 30px rgba(102, 126, 234, 0.3)' : 'none',
            transform: isEditing ? 'none' : 'none',
            transition: isEditing ? 'none' : 'all 0.3s ease',
            borderRadius: '2px',
            backdropFilter: isGlass ? 'blur(8px)' : 'none'
          };
        } else {
          // 原有样式
          const noteBoxShadow = (comp?.noteStyle === 'white' && comp?.noteBgColor) ? (() => {
            const r = Math.max(0, parseInt(comp.noteBgColor.slice(1,3), 16));
            const g = Math.max(0, parseInt(comp.noteBgColor.slice(3,5), 16));
            const b = Math.max(0, parseInt(comp.noteBgColor.slice(5,7), 16));
            return "0 10px 30px rgba(" + r + "," + g + "," + b + ",0.15), 0 0 10px rgba(" + r + "," + g + "," + b + ",0.05) inset";
          })() : currentStyle.boxShadow;
          noteContainerStyle = {
            ...baseStyle,
            padding: notePaddingTop + "px " + notePaddingRight + "px " + notePaddingBottom + "px " + notePaddingLeft + "px",
            background: (comp?.noteStyle === 'white' && comp?.noteBgColor) ? comp.noteBgColor : currentStyle.texture,
            borderLeft: 'none',
            borderTop: isEditing ? tc('borderDashed') : 'none',
            borderRight: 'none',
            borderBottom: 'none',
            boxShadow: isEditing ? '0 10px 30px rgba(102, 126, 234, 0.3)' : noteBoxShadow,
            transform: isEditing ? 'none' : (enableTilt ? `rotate(${currentStyle.rotation}deg)` : 'none'),
            transition: isEditing ? 'none' : 'all 0.3s ease',
            borderRadius: '2px',
            backdropFilter: isGlass ? currentStyle.backdropFilter : 'none'
          };
        }

        return (
          <div
            style={noteContainerStyle}
            data-component-content="true"
onMouseEnter={(e) => {
              if (!isEditing && enableTilt && !isGlass) {
                e.currentTarget.style.transform = 'rotate(0deg)';
                const bgRgb = (comp?.noteStyle === 'white' && comp?.noteBgColor) ? { r: parseInt(comp.noteBgColor.slice(1,3), 16), g: parseInt(comp.noteBgColor.slice(3,5), 16), b: parseInt(comp.noteBgColor.slice(5,7), 16) } : { r: 0, g: 0, b: 0 };
                e.currentTarget.style.boxShadow = "0 15px 35px rgba(" + bgRgb.r + "," + bgRgb.g + "," + bgRgb.b + ",0.2)";
              }
            }}
            onMouseLeave={(e) => {
              if (!isEditing && enableTilt && !isGlass) {
                e.currentTarget.style.transform = `rotate(${currentStyle.rotation}deg)`;
                e.currentTarget.style.boxShadow = currentStyle.boxShadow;
              }
            }}
          >
            {resizeHandles}
            {editButtons}
            <style>{"@keyframes none{} .note-scroll::-webkit-scrollbar{width:4px} .note-scroll::-webkit-scrollbar-track{background:transparent} .note-scroll::-webkit-scrollbar-thumb{background:rgba(0,0,0,0.08);border-radius:2px} .note-scroll::-webkit-scrollbar-thumb:hover{background:rgba(0,0,0,0.15)} .note-scroll { scrollbar-width: thin; scrollbar-color: rgba(0,0,0,0.08) transparent; }"}</style>
            {!isEditing && enableFold && !isGlass && (
              <div style={{
                position: 'absolute',
                top: 0,
                right: 0,
                width: 0,
                height: 0,
                borderStyle: 'solid',
                borderWidth: '0 30px 30px 0',
                borderColor: 'transparent rgba(0,0,0,0.06) transparent transparent',
                pointerEvents: 'none'
              }} />
            )}
            <div className="note-scroll" style={{ ...contentContainerStyle, overflowY: 'auto', overflowX: 'hidden' }}>
              {comp?.showTitle !== false && (
                <h3
                  style={{
                    margin: '0 0 12px 0',
                    fontSize: '16px',
                    fontWeight: '600',
                    flexShrink: 0,
                    color: currentStyle.textColor
                  }}
                  dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '便笺') }}
                />
              )}
              <div
                contentEditable={!isEditing}
                style={{
                  fontSize: currentFontSize + 'px',
                  fontFamily: currentFontFamily,
                  color: currentStyle.textColor,
                  minHeight: '120px',
                  outline: 'none',
                  cursor: isEditing ? 'move' : 'text',
                  lineHeight: '1.6'
                }}
                suppressContentEditableWarning={true}
                onInput={(e) => {
                  if (!isEditing) {
                    updateComponent(component.id, { content: e.currentTarget.innerHTML });
                  }
                }}
                onBlur={async (e) => {
                  if (!isEditing) {
                    // 自动保存
                    const newConfig = tempConfig || config;
                    const compIndex = newConfig.components.findIndex(c => c.id === component.id);
                    if (compIndex !== -1) {
                      newConfig.components[compIndex].content = e.currentTarget.innerHTML;
                      await saveConfig(newConfig);
                    }
                  }
                }}
                dangerouslySetInnerHTML={{ __html: sanitizeNoteContent(comp?.content || '点击这里开始编辑...') }}
              />
            </div>
          </div>
        );
      }

      case 'search': {
        // 获取外框样式设置
        const backgroundStyle = comp?.backgroundStyle || 'glass';
        const bgColor = comp?.bgColor || '#ffffff';
        const bgOpacity = comp?.bgOpacity ?? 0.9;
        const borderRadius = comp?.borderRadius ?? 24;

        // 根据背景样式创建不同的组件样式
        let searchBaseStyle;
        if (backgroundStyle === 'glass') {
          searchBaseStyle = { ...baseStyle, borderRadius: borderRadius + 'px' };
        } else if (backgroundStyle === 'softShadow') {
          // 柔边阴影样式
          searchBaseStyle = {
            ...baseStyle,
            background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`,
            backdropFilter: 'none',
            boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none',
            border: isEditing ? tc('borderDashed') : 'none',
            borderRadius: borderRadius + 'px'
          };
        } else {
          searchBaseStyle = { ...baseStyle, borderRadius: borderRadius + 'px' };
        }

        // 搜索输入框组件 - 使用主组件中存储的状态
        const { useMemo, useEffect } = dc;
        const state = getSearchState(component.id);
        const { searchQuery, showHelp, contentResults, selectedIndex } = state;

        // 解析搜索输入并构建 datacore 查询
        const searchConfig = useMemo(() => {
          if (!searchQuery.trim()) {
            return { type: 'none', query: null, searchTerm: '' };
          }

          const input = searchQuery;

          // 任务搜索: task:关键词
          if (input.startsWith('task:')) {
            const keyword = input.replace(/^task:/i, '').trim();
            if (!keyword) return { type: 'none', query: null, searchTerm: '' };
            return {
              type: 'task',
              query: '@task',
              searchTerm: keyword
            };
          }

          // 内容搜索: content:关键词（使用 vault API）
          if (input.startsWith('content:')) {
            const keyword = input.replace(/^content:/i, '').trim();
            if (!keyword) return { type: 'none', searchTerm: '' };
            return {
              type: 'content',
              searchTerm: keyword
            };
          }

          // 标签搜索: tag:标签（实时模糊匹配）
          if (input.startsWith('tag:')) {
            const keyword = input.replace(/^tag:#?/i, '').trim();
            if (!keyword) return { type: 'none', query: null, searchTerm: '' };
            return {
              type: 'tag',
              query: '@page', // 查询所有页面，然后在 JavaScript 中模糊过滤
              searchTerm: keyword
            };
          }

          // 路径搜索: path:关键词
          if (input.startsWith('path:')) {
            const keyword = input.replace(/^path:/i, '').trim();
            if (!keyword) return { type: 'none', query: null, searchTerm: '' };
            return {
              type: 'path',
              query: '@page',
              searchTerm: keyword
            };
          }

          // 属性搜索: prop:名=值 或 prop:名
          if (input.startsWith('prop:') || input.startsWith('property:')) {
            const rest = input.replace(/^(prop|property):/i, '').trim();
            if (!rest) return { type: 'none', query: null, searchTerm: '' };
            const parts = rest.split('=');
            if (parts.length === 2) {
              const propName = parts[0].trim();
              const propValue = parts[1].trim();
              if (!propName || !propValue) return { type: 'none', query: null, searchTerm: '' };
              // 属性值模糊匹配：查询有该属性的页面，然后在 JavaScript 中过滤值
              return {
                type: 'prop-value',
                query: `@page and exists(${propName})`,
                searchTerm: `${propName}=${propValue}`,
                propName,
                propValue
              };
            } else {
              // 精确匹配属性名
              const propName = parts[0].trim();
              if (!propName) return { type: 'none', query: null, searchTerm: '' };
              return {
                type: 'prop-name',
                query: `@page and exists(${propName})`,
                searchTerm: propName,
                propName
              };
            }
          }

          // 命令模式: /命令名
          if (input.startsWith('/')) {
            const keyword = input.substring(1).trim();
            if (!keyword) return { type: 'command', searchTerm: '' };
            return {
              type: 'command',
              searchTerm: keyword
            };
          }

          // 默认：文件名搜索
          return {
            type: 'default',
            query: '@page',
            searchTerm: input
          };
        }, [searchQuery]);

        // 执行 datacore 查询 - 用 useMemo 缓存，仅在 query 变化时重新订阅
        const queryResults = useMemo(() => {
          const queryStr = searchConfig.query;
          if (!queryStr || typeof queryStr !== 'string' || !queryStr.includes('@')) return [];
          try {
            return dc.useQuery(queryStr);
          } catch (e) {
            console.error('搜索查询失败:', e);
            return [];
          }
        }, [searchConfig.query]);

        // 内容搜索使用 vault API（异步）
        useEffect(() => {
          // 中文输入法输入过程中不执行搜索，避免闪烁
          if (state.isComposing) {
            return;
          }

          if (searchConfig.type === 'content') {
            const searchContent = async () => {
              const keyword = searchConfig.searchTerm.toLowerCase();
              if (!keyword) {
                updateSearchState(component.id, { contentResults: [] });
                return;
              }

              const allFiles = vault.getMarkdownFiles();
              const results = [];
              const maxMatches = 3;  // 每个文件最多显示3个匹配

              // 提取关键词周围的上下文
              const extractContext = (text, keyword, index) => {
                const beforeLen = 35;   // 关键词前保留字符数
                const afterLen = 40;    // 关键词后保留字符数

                const start = Math.max(0, index - beforeLen);
                const end = Math.min(text.length, index + keyword.length + afterLen);
                let context = text.substring(start, end);

                // 计算关键词在上下文中的位置
                let keywordStart = index - start;

                // 添加省略号
                if (start > 0) {
                  context = '...' + context;
                  keywordStart += 3;
                }
                if (end < text.length) {
                  context = context + '...';
                }

                return { context, keywordStart, keywordLen: keyword.length };
              };

              // 查找文本中所有匹配的位置
              const findAllMatches = (text, keyword) => {
                const matches = [];
                const lowerText = text.toLowerCase();
                let index = 0;

                while ((index = lowerText.indexOf(keyword, index)) !== -1) {
                  matches.push(index);
                  index += keyword.length;  // 移动到关键词后面
                }

                return matches;
              };

              for (const file of allFiles) {
                try {
                  const content = await vault.cachedRead(file);
                  const matchIndexes = findAllMatches(content, keyword);

                  if (matchIndexes.length > 0) {
                    // 只取前3个匹配
                    const matches = matchIndexes.slice(0, maxMatches).map(index =>
                      extractContext(content, keyword, index)
                    );

                    results.push({
                      $file: file.path,
                      $name: file.basename,
                      $path: file.path,
                      $text: content,
                      _matches: matches,
                      _hasMore: matchIndexes.length > maxMatches  // 是否有更多匹配
                    });
                  }
                } catch (err) {
                  // 忽略读取失败的文件
                }
              }

              updateSearchState(component.id, { contentResults: results });
            };

            searchContent();
          } else {
            updateSearchState(component.id, { contentResults: [] });
          }
        }, [searchConfig.type, searchConfig.searchTerm, state.isComposing]);

        // 标签和属性搜索需要在 JavaScript 中进行模糊过滤
        // 使用 queryResults.length 作为稳定依赖，避免因数组引用变化导致无限循环
        const results = dc.useMemo(() => {
          // 命令模式：匹配 Obsidian 命令
          if (searchConfig.type === 'command') {
            const commandsResult = commands.listCommands();
            const allCommands = Array.isArray(commandsResult) ? commandsResult : [];
            const searchTerm = searchConfig.searchTerm.toLowerCase();
            return allCommands
              .filter(cmd => cmd.name.toLowerCase().includes(searchTerm))
              .slice(0, comp?.maxItems || 20);
          }

          // 文件名搜索（大小写不敏感，按匹配度排序）
          if (searchConfig.type === 'default') {
            const searchTerm = searchConfig.searchTerm.toLowerCase();
            return queryResults
              .filter(page => page.$name.toLowerCase().includes(searchTerm))
              .map(page => {
                const name = page.$name.toLowerCase();
                let score = 0;
                if (name === searchTerm) score = 0;            // 完全匹配
                else if (name.startsWith(searchTerm)) score = 1; // 前缀匹配
                else score = 2 + name.indexOf(searchTerm);      // 包含匹配，位置越靠前分越低
                score = score * 10000 + name.length;            // 同级别时短文件名优先
                return { page, score };
              })
              .sort((a, b) => a.score - b.score)
              .map(item => item.page)
              .slice(0, comp?.maxItems || 20);
          }

          // 任务搜索（大小写不敏感）
          if (searchConfig.type === 'task') {
            const searchTerm = searchConfig.searchTerm.toLowerCase();
            return queryResults
              .filter(task => (task.$text || '').toLowerCase().includes(searchTerm))
              .slice(0, comp?.maxItems || 20);
          }

          // 路径搜索（大小写不敏感）
          if (searchConfig.type === 'path') {
            const searchTerm = searchConfig.searchTerm.toLowerCase();
            return queryResults
              .filter(page => page.$path.toLowerCase().includes(searchTerm))
              .slice(0, comp?.maxItems || 20);
          }

          // 内容搜索：使用 vault API 的结果
          if (searchConfig.type === 'content') {
            return contentResults;
          }

          if (searchConfig.type === 'tag') {
            return queryResults.filter(page => {
              const tags = page.value('tags');
              const searchTerm = searchConfig.searchTerm.toLowerCase();

              // 处理字符串格式：tags: daily
              if (typeof tags === 'string') {
                return tags.toLowerCase().replace('#', '').includes(searchTerm);
              }

              // 处理数组格式：tags: - "clippings"
              if (Array.isArray(tags)) {
                return tags.some(tag => {
                  const tagStr = String(tag).toLowerCase().replace('#', '');
                  return tagStr.includes(searchTerm);
                });
              }

              return false;
            });
          }

          // prop-name 类型直接返回查询结果（已通过 exists 精确过滤）
          // 不需要额外过滤

          // 属性值模糊搜索
          if (searchConfig.type === 'prop-value') {
            const { propName, propValue } = searchConfig;
            const searchTerm = propValue.toLowerCase();
            return queryResults.filter(page => {
              const value = page.value(propName);
              if (value === undefined || value === null) return false;
              return String(value).toLowerCase().includes(searchTerm);
            });
          }

          return queryResults;
        }, [queryResults.length, contentResults, searchConfig.type, searchConfig.searchTerm, searchConfig.propName, searchConfig.propValue]);

        // 获取搜索类型标签
        const getSearchTypeLabel = () => {
          if (!searchQuery.trim()) return '';
          switch (searchConfig.type) {
            case 'task': return '✅ 任务搜索';
            case 'content': return '📝 内容搜索';
            case 'tag': return '🏷️ 标签搜索';
            case 'prop-name': return '📋 属性名搜索';
            case 'prop-value': return '📋 属性值搜索';
            case 'path': return '📁 路径搜索';
            case 'command': return '⌨️ 命令模式';
            default: return '🔍 文件名搜索';
          }
        };

        return (
          <div
            style={{
              ...searchBaseStyle,
              padding: '16px 20px',
              alignItems: 'flex-start',
              height: 'auto',
              minHeight: comp?.height || 400,
              display: 'flex',
              flexDirection: 'column'
            }}
            data-component-content="true"
          >
            {resizeHandles}
            {editButtons}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
              width: '100%',
              height: '100%'
            }}>
              {/* 搜索输入框 */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px'
                }}>
                  <span style={{ fontSize: '20px' }}>🔎</span>
                  <div style={{ flex: 1, position: 'relative' }}>
                  <input
                    type="text"
                    placeholder={comp?.placeholder || '搜索笔记...'}
                    value={searchQuery}
                    onChange={(e) => {
                      // 中文输入法输入过程中只更新输入框值，不触发搜索
                      // 在 onCompositionEnd 时才会真正触发搜索
                      updateSearchState(component.id, { searchQuery: e.target.value, selectedIndex: 0 });
                    }}
                    onCompositionStart={(e) => {
                      updateSearchState(component.id, { isComposing: true });
                    }}
                    onCompositionEnd={(e) => {
                      updateSearchState(component.id, {
                        isComposing: false,
                        searchQuery: e.target.value,
                        selectedIndex: 0
                      });
                    }}
                    onKeyDown={(e) => {
                      if (searchConfig.type === 'command' && results.length > 0) {
                        if (e.key === 'ArrowDown') {
                          e.preventDefault();
                          updateSearchState(component.id, { selectedIndex: (state.selectedIndex + 1) % results.length });
                        } else if (e.key === 'ArrowUp') {
                          e.preventDefault();
                          updateSearchState(component.id, { selectedIndex: (state.selectedIndex - 1 + results.length) % results.length });
                        } else if (e.key === 'Enter') {
                          e.preventDefault();
                          commands.executeCommandById(results[selectedIndex].id);
                          updateSearchState(component.id, { searchQuery: '', selectedIndex: 0 });
                        }
                      }
                    }}
                    style={{
                      width: '100%',
                      padding: '10px 16px',
                      paddingRight: searchQuery ? '36px' : '16px',
                      border: 'none',
                      borderRadius: '16px',
                      fontSize: '14px',
                      background: tc('cardBgMedium'),
                      outline: 'none',
                      boxSizing: 'border-box'
                    }}
                    onFocus={(e) => {
                      e.currentTarget.style.background = tc('cardBgHeavy');
                    }}
                    onBlur={(e) => {
                      e.currentTarget.style.background = tc('cardBgMedium');
                    }}
                  />
                  {searchQuery && (
                    <span
                      onClick={() => updateSearchState(component.id, { searchQuery: '', selectedIndex: 0 })}
                      style={{
                        position: 'absolute',
                        right: '10px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        cursor: 'pointer',
                        fontSize: '16px',
                        color: '#999',
                        lineHeight: '1',
                        userSelect: 'none'
                      }}
                    >&#10005;</span>
                  )}
                  </div>
                  <button
                    onClick={() => updateSearchState(component.id, { showHelp: !state.showHelp })}
                    style={{
                      padding: '8px 12px',
                      background: tc('cardBgLight'),
                      border: 'none',
                      borderRadius: '12px',
                      fontSize: '12px',
                      cursor: 'pointer',
                      whiteSpace: 'nowrap'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = tc('cardBgMedium')}
                    onMouseLeave={(e) => e.currentTarget.style.background = tc('cardBgLight')}
                  >
                    {showHelp ? '隐藏帮助' : '帮助'}
                  </button>
                </div>

                {/* 搜索类型提示和调试信息 */}
                {searchQuery.trim() && (
                  <div style={{
                    padding: '6px 10px',
                    background: tc('successBg'),
                    borderRadius: '8px',
                    fontSize: '11px',
                    color: tc('successText')
                  }}>
                    {getSearchTypeLabel()}
                  </div>
                )}

                {/* 帮助提示 */}
                {showHelp && (
                  <div style={{
                    padding: '8px 12px',
                    background: tc('cardBgSubtle'),
                    borderRadius: '8px',
                    fontSize: '11px',
                    color: tc('textMuted')
                  }}>
                    <div style={{ marginBottom: '4px', fontWeight: '500' }}>搜索语法：</div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '4px' }}>
                      <div><code>/命令</code> - 命令模式</div>
                      <div><code>task:关键词</code> - 任务</div>
                      <div><code>content:关键词</code> - 内容</div>
                      <div><code>tag:标签</code> - 标签</div>
                      <div><code>prop:名=值</code> - 属性值</div>
                      <div><code>prop:名</code> - 属性名</div>
                      <div><code>path:路径</code> - 路径</div>
                      <div><code>直接输入</code> - 文件名</div>
                    </div>
                    <div style={{ marginTop: '6px', paddingTop: '6px', borderTop: '1px solid rgba(0,0,0,0.1)', fontSize: '10px' }}>
                      属性名精确匹配，属性值、标签、命令支持模糊匹配
                    </div>
                  </div>
                )}
              </div>

              {/* 搜索结果 */}
              <div style={{
                flex: 1,
                maxHeight: '600px',
                overflowY: 'auto',
                overflowX: 'auto',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
                scrollbarWidth: 'thin',
                scrollbarColor: 'rgba(0, 0, 0, 0.2) transparent',
                WebkitScrollbarWidth: 'thin',
                MsOverflowStyle: 'thin'
              }}>
                {searchQuery.trim() ? (
                  results.length === 0 ? (
                    <div style={{
                      padding: '16px',
                      textAlign: 'center',
                      color: tc('textMuted'),
                      fontSize: '13px'
                    }}>
                      未找到相关笔记
                    </div>
                  ) : (
                    <>
                      <div style={{
                        fontSize: '12px',
                        color: tc('textMuted'),
                        padding: '4px 8px'
                      }}>
                        找到 {results.length} 条结果
                      </div>
                      {results.slice(0, comp?.maxItems || 20).map((result, idx) => {
                        // 根据搜索类型提取不同信息
                        let icon = '📄';
                        let displayName = '';
                        let displayPath = '';
                        let matchContent = '';

                        if (searchConfig.type === 'command') {
                          // 命令模式结果 - 不显示图标和路径
                          icon = '';
                          displayName = result.name;
                          displayPath = '';
                          matchContent = '';
                        } else if (searchConfig.type === 'task') {
                          // 任务结果 - 任务是 block 类型，使用 $file 获取文件路径
                          icon = '✅';
                          displayName = result.$text || '任务';
                          displayPath = result.$file || '';  // 直接使用 $file 获取文件路径
                          matchContent = ''; // 不显示第三行
                        } else if (searchConfig.type === 'content') {
                          // 内容搜索结果 - 使用 vault API
                          icon = '📝';
                          displayName = result.$name || '未知';
                          displayPath = result.$path || '';
                          // matchContent 由 _matches 数组处理，这里设为占位值
                          matchContent = 'has_matches';
                        } else {
                          // 页面结果
                          icon = '📄';
                          displayName = result.value('title') || result.value('$name') || result.$name || '';
                          displayPath = result.$path || '';

                          // 根据搜索类型显示匹配内容
                          if (searchConfig.type === 'tag') {
                            const tags = result.value('tags');
                            // 显示该笔记的所有标签
                            if (tags) {
                              if (typeof tags === 'string') {
                                matchContent = `标签: ${tags.startsWith('#') ? tags : '#' + tags}`;
                              } else if (Array.isArray(tags) && tags.length > 0) {
                                const tagList = tags.map(t => t.startsWith('#') ? t : '#' + t).join(' ');
                                matchContent = `标签: ${tagList}`;
                              }
                            }
                          } else if (searchConfig.type === 'prop-name') {
                            // 显示属性名和值
                            const { propName } = searchConfig;
                            const value = result.value(propName);
                            if (value !== undefined && value !== null) {
                              matchContent = `${propName}: ${value}`;
                            } else {
                              matchContent = `${propName}: (无值)`;
                            }
                          } else if (searchConfig.type === 'prop-value') {
                            // 显示属性名和值
                            const { propName, propValue } = searchConfig;
                            const value = result.value(propName);
                            if (value !== undefined && value !== null) {
                              matchContent = `${propName}: ${value}`;
                            }
                          } else if (searchConfig.type === 'path') {
                            // 不显示第三行
                            matchContent = '';
                          }
                        }

                        return (
                          <div
                            key={idx}
                            onClick={() => {
                              if (isEditing) return;
                              if (searchConfig.type === 'command') {
                                commands.executeCommandById(result.id);
                                updateSearchState(component.id, { searchQuery: '', selectedIndex: 0 });
                              } else if (displayPath) {
                                openFile(displayPath);
                              }
                            }}
                            style={{
                              padding: searchConfig.type === 'command' ? '10px 14px' : '12px 14px',
                              background: searchConfig.type === 'command' && idx === selectedIndex
                                ? tc('accentBgHover')
                                : tc('cardBgLight'),
                              borderRadius: '12px',
                              cursor: isEditing ? 'move' : 'pointer',
                              fontSize: '13px',
                              transition: 'all 0.2s',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: '6px'
                            }}
                            onMouseEnter={(e) => {
                              if (!isEditing) {
                                if (searchConfig.type === 'command') {
                                  updateSearchState(component.id, { selectedIndex: idx });
                                } else {
                                  e.currentTarget.style.background = tc('cardBgMedium');
                                }
                              }
                            }}
                            onMouseLeave={(e) => {
                              if (!isEditing && searchConfig.type !== 'command') {
                                e.currentTarget.style.background = tc('cardBgLight');
                              }
                            }}
                          >
                            {/* 第一行：图标 + 名称 */}
                            <div style={{ display: 'flex', alignItems: 'center', gap: icon ? '8px' : '0' }}>
                              {icon && <span style={{ fontSize: '16px', flexShrink: 0 }}>{icon}</span>}
                              <span style={{
                                flex: 1,
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap',
                                fontWeight: '500'
                              }}>
                                {displayName}
                              </span>
                            </div>
                            {/* 第二行：路径 */}
                            {displayPath && (
                              <div style={{
                                fontSize: '11px',
                                color: tc('textMuted'),
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap',
                                paddingLeft: '24px'
                              }}>
                                {displayPath}
                              </div>
                            )}
                            {/* 第三行：匹配内容 */}
                            {matchContent && searchConfig.type === 'content' && result._matches ? (
                              <div style={{ paddingLeft: '24px' }}>
                                {result._matches.map((match, matchIdx) => (
                                  <div key={matchIdx} style={{
                                    fontSize: '11px',
                                    color: tc('accent'),
                                    marginBottom: matchIdx < result._matches.length - 1 ? '4px' : '0'
                                  }}>
                                    {match.context.substring(0, match.keywordStart)}
                                    <strong style={{
                                      background: 'rgba(255, 230, 0, 0.4)',
                                      padding: '0 2px',
                                      borderRadius: '2px'
                                    }}>
                                      {match.context.substring(match.keywordStart, match.keywordStart + match.keywordLen)}
                                    </strong>
                                    {match.context.substring(match.keywordStart + match.keywordLen)}
                                  </div>
                                ))}
                                {result._hasMore && (
                                  <div style={{
                                    fontSize: '11px',
                                    color: tc('textFaint'),
                                    fontStyle: 'italic'
                                  }}>
                                    ...
                                  </div>
                                )}
                              </div>
                            ) : matchContent ? (
                              <div style={{
                                fontSize: '11px',
                                color: tc('accent'),
                                paddingLeft: '24px'
                              }}>
                                {matchContent}
                              </div>
                            ) : null}
                          </div>
                        );
                      })}
                    </>
                  )
                ) : (
                  <div style={{
                    flex: 1,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: tc('textFaint'),
                    fontSize: '13px'
                  }}>
                    输入关键词开始搜索
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      }

      case 'personal': {
        // 图标SVG
        const icons = {
          blog: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 28 28"><path stroke="currentColor" stroke-width="1.5" d="M24.733 5.911c-.155-1.555-1.089-2.333-2.644-2.333H8.4c-1.711 0-3.111 1.244-3.111 3.11v13.379H3.11v1.555c0 1.867 1.245 2.956 2.956 2.956h13.222c.311 0 .778-.156 1.089-.156 1.089-.466 1.71-1.4 1.71-2.8V10.111h2.49c.155-1.555.31-2.955.155-4.2m-7.31 17.111h-11.2c-1.09 0-1.712-.622-1.712-1.555v-.156h12.6c.156.622.311 1.089.467 1.711zM8.4 13.844c0-.466.311-.622.778-.622h4.355c.467 0 .778.311.778.622 0 .467-.311.778-.778.778h-4.51c-.312-.155-.623-.31-.623-.778m9.644-3.11H9.022c-.466 0-.778-.312-.778-.623.156-.467.312-.778.778-.778h9.022c.623 0 1.09.311 1.09.778 0 .311-.312.622-1.09.622m5.29-2.178h-1.09v-2.8c0-.312.311-.467.467-.467.311 0 .467.311.467.467v2.8z"/></svg>',
          project: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 28 28"><path stroke="currentColor" stroke-width="1.5" d="M4.426 17.494h5.745c.144 0 .238.039.335.131a.33.33 0 0 1 .115.275v5.694c0 .12-.03.191-.115.274a.43.43 0 0 1-.335.132H4.426a.4.4 0 0 1-.314-.122C4.035 23.802 4 23.73 4 23.594V17.9a.36.36 0 0 1 .118-.29c.078-.077.156-.116.308-.116Zm11.515 0h5.744c.107 0 .18.021.248.067l.065.055a.35.35 0 0 1 .112.284v5.694a.36.36 0 0 1-.115.287.39.39 0 0 1-.31.119H15.94a.44.44 0 0 1-.335-.132.33.33 0 0 1-.115-.274V17.9c0-.12.03-.192.115-.275a.43.43 0 0 1 .335-.13ZM19.195 4c.107 0 .197.023.287.084l.092.074 4.264 4.201v.001c.128.127.162.23.162.353 0 .124-.033.212-.145.316l-.008.008-.01.009-4.276 4.219c-.133.131-.239.166-.364.166-.127 0-.234-.037-.361-.163l-.003-.003-4.275-4.22a.42.42 0 0 1-.14-.332c0-.107.023-.194.082-.28l.072-.087 4.247-4.19A.5.5 0 0 1 19.195 4ZM4.425 6.155h5.746c.144 0 .238.04.335.132.083.08.115.148.115.275v5.67a.37.37 0 0 1-.128.298.4.4 0 0 1-.322.132H4.426a.37.37 0 0 1-.3-.119h.002A.4.4 0 0 1 4 12.231v-5.67l.007-.087a.35.35 0 0 1 .108-.2.4.4 0 0 1 .31-.119Z"/></svg>',
          smile: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 28 28"><circle cx="14" cy="14" r="10" stroke="currentColor" stroke-width="1.6"></circle><path stroke="currentColor" stroke-linecap="round" stroke-width="1.5" d="M10 18c2.5 2.5 5.5 2.5 8 0"/></svg>',
          star: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 28 28"><path fill="currentColor" d="M7.59 25.25c-.287 0-.57-.09-.814-.266a1.38 1.38 0 0 1-.57-1.237l.51-6.34-4.139-4.83a1.38 1.38 0 0 1-.266-1.335 1.38 1.38 0 0 1 1-.923l6.188-1.475 3.314-5.429A1.38 1.38 0 0 1 14 2.75c.488 0 .932.249 1.187.666l3.314 5.43 6.188 1.474a1.38 1.38 0 0 1 1 .923c.151.465.052.964-.267 1.335l-4.139 4.83.51 6.34c.039.487-.174.95-.57 1.237-.394.287-.899.347-1.351.158L14 22.698l-5.873 2.444a1.4 1.4 0 0 1-.536.109M14 21.037q.273 0 .533.107l5.591 2.327-.484-6.036a1.4 1.4 0 0 1 .33-1.015l3.94-4.599-5.89-1.404a1.4 1.4 0 0 1-.865-.628L14 4.62l-3.155 5.168a1.4 1.4 0 0 1-.866.628L4.09 11.82l3.941 4.598c.239.279.36.649.33 1.016l-.485 6.036 5.59-2.326q.261-.108.535-.108M18.398 8.82h.002z"/></svg>',
          globe: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 28 28"><path fill="currentColor" d="M3 14a11 11 0 1 1 22 0 11 11 0 0 1-22 0m8.142-9.025a9.45 9.45 0 0 0-3.33 1.862c.614.53 1.293.982 2.026 1.341.162-.609.348-1.178.555-1.699.221-.549.47-1.059.75-1.504M6.734 7.931a9.42 9.42 0 0 0-2.168 5.302h4.586c.035-1.238.156-2.422.351-3.518a11 11 0 0 1-2.769-1.78zm10.124 15.094a9.5 9.5 0 0 0 3.33-1.864 9.5 9.5 0 0 0-2.026-1.341q-.226.867-.555 1.699c-.22.55-.47 1.058-.75 1.504zm4.408-2.961a9.4 9.4 0 0 0 2.169-5.297H18.85a24 24 0 0 1-.353 3.517 11.1 11.1 0 0 1 2.769 1.782zm2.169-6.831a9.42 9.42 0 0 0-2.17-5.299 11 11 0 0 1-2.767 1.78c.194 1.097.315 2.281.352 3.519zm-3.25-6.396a9.45 9.45 0 0 0-3.33-1.863c.28.448.53.956.75 1.505q.314.784.554 1.7a9.5 9.5 0 0 0 2.026-1.342m-9.043 16.19a9.6 9.6 0 0 1-.749-1.506 15 15 0 0 1-.554-1.7 9.5 9.5 0 0 0-2.026 1.342 9.45 9.45 0 0 0 3.33 1.863m-4.406-2.961a11 11 0 0 1 2.767-1.78 24 24 0 0 1-.353-3.519H4.567a9.42 9.42 0 0 0 2.17 5.299zM14 4.535c-.286 0-.635.143-1.036.565-.4.423-.797 1.077-1.145 1.949a13 13 0 0 0-.54 1.694c.883.264 1.8.397 2.721.396.947 0 1.86-.138 2.723-.396a13 13 0 0 0-.54-1.693c-.35-.873-.746-1.527-1.147-1.95-.4-.422-.749-.565-1.036-.565m-3.314 8.698h6.628q-.043-1.501-.281-2.982c-.986.281-2.007.424-3.033.423-1.025 0-2.046-.142-3.031-.423q-.24 1.48-.284 2.982zm.283 4.517A11 11 0 0 1 14 17.326c1.051 0 2.069.147 3.033.424.15-.927.248-1.93.28-2.983h-6.627c.033 1.053.13 2.057.283 2.983M14 18.86a9.5 9.5 0 0 0-2.721.397c.155.618.337 1.186.54 1.693.348.873.744 1.527 1.145 1.95.4.422.75.565 1.036.565s.637-.143 1.036-.565c.4-.423.798-1.077 1.147-1.949q.304-.763.538-1.694A9.5 9.5 0 0 0 14 18.86"/></svg>'
        };

        // 获取头像图片路径
        const getAvatarSrc = () => {
          const src = comp?.avatar || '';
          if (!src) return null;

          // 直接返回各种 URL 格式
          if (src.startsWith('http://') || src.startsWith('https://') ||
              src.startsWith('data:') || src.startsWith('file:') ||
              src.startsWith('blob:')) {
            return src;
          }

          // 如果是 Obsidian 附件路径
          const file = vault.getAbstractFileByPath(src);
          if (file) {
            return vault.getResourcePath(file);
          }

          // 尝试作为相对路径处理
          return src;
        };

        const avatarSrc = getAvatarSrc();

        // 处理菜单项点击
        const handleMenuClick = (item) => {
          if (isEditing) return;
          executeLinkAction({ link: item.link, linkMode: item.linkMode, commandId: item.commandId, commands, onNavigate: (link) => {
            const openTarget = item.openTarget || 'mini';
            if (openTarget === 'tab') {
              workspace.openLinkText(link, currentFilePath, 'tab');
            } else {
              let filePath = link;
              const hashIndex = link.indexOf('#');
              if (hashIndex !== -1) filePath = link.substring(0, hashIndex);
              const file = vault.getAbstractFileByPath(filePath);
              if (file) { setViewMode(true); setCurrentViewingFile(link); setViewingPersonalComponentId(comp.id); }
              else openFile(link);
            }
          }});
        };

        const menuItems = comp?.menuItems || [];

        // 获取背景样式设置
        const backgroundStyle = comp?.backgroundStyle || 'glass';
        const bgColor = comp?.bgColor || '#ffffff';
        const bgOpacity = comp?.bgOpacity ?? 0.9;

        // 根据背景样式创建不同的卡片样式
        let cardBaseStyle;
        if (backgroundStyle === 'glass') {
          cardBaseStyle = baseStyle;
        } else if (backgroundStyle === 'softShadow') {
          // 柔边阴影样式 - 保持与毛玻璃样式相同的 borderRadius 和 padding，确保内部元素位置不变
          cardBaseStyle = {
            ...baseStyle,
            background: `rgba(${parseInt(bgColor.slice(1, 3), 16)}, ${parseInt(bgColor.slice(3, 5), 16)}, ${parseInt(bgColor.slice(5, 7), 16)}, ${bgOpacity})`,
            backdropFilter: 'none',
            boxShadow: comp?.showBorder !== false ? tc('shadowSoft') : 'none',
            border: isEditing ? tc('borderDashed') : 'none'
          };
        } else {
          // 默认毛玻璃样式
          cardBaseStyle = baseStyle;
        }

        return (
          <div style={cardBaseStyle} data-component-content="true">
            {resizeHandles}
            {editButtons}
            <div style={contentContainerStyle}>
              {/* 头像和名字 */}
              {comp?.showPersonalInfo !== false && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px', flexShrink: 0 }}>
                {avatarSrc ? (
                  <div style={{
                    width: '64px',
                    height: '64px',
                    borderRadius: '50%',
                    overflow: 'hidden',
                    flexShrink: 0
                  }}>
                    <img src={avatarSrc} alt="头像" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  </div>
                ) : (
                  <div style={{
                    width: '64px',
                    height: '64px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '32px',
                    color: '#fff',
                    flexShrink: 0
                  }}>
                    👤
                  </div>
                )}
                <div style={{ minWidth: 0 }}>
                  <div style={{
                    fontSize: (comp?.nameFontSize || 24) + 'px',
                    fontWeight: '700',
                    color: comp?.nameColor || tc('nameColor'),
                    fontFamily: comp?.nameFontFamily || undefined,
                    lineHeight: '1.2'
                  }}>
                    {comp?.name || '你的名字'}
                  </div>
                  {comp?.tagline && (
                    <div style={{
                      fontSize: (comp?.taglineFontSize || 14) + 'px',
                      fontWeight: '500',
                      color: comp?.taglineColor || tc('taglineColor'),
                      fontFamily: comp?.taglineFontFamily || undefined,
                      marginTop: '4px'
                    }}>
                      {comp.tagline}
                    </div>
                  )}
                </div>
              </div>
              )}

              {/* 菜单列表 */}
              {menuItems.length > 0 && (
                <div>
                  {menuItems.map((item, idx) => (
                    <div
                      key={idx}
                      onClick={() => handleMenuClick(item)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        padding: '12px 16px',
                        borderRadius: '16px',
                        cursor: isEditing ? 'move' : 'pointer',
                        transition: 'all 0.2s',
                        color: comp?.menuFontColor || tc('menuFontColor'),
                        textDecoration: 'none',
                        marginBottom: '4px'
                      }}
                      onMouseEnter={(e) => {
                        if (!isEditing) {
                          e.currentTarget.style.background = tc('menuHoverBg');
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (!isEditing) {
                          e.currentTarget.style.background = 'transparent';
                        }
                      }}
                    >
                      <span style={{
                        width: '24px',
                        height: '24px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0
                      }}>
                        <dc.Icon icon={item.icon} />
                      </span>
                      <span style={{ fontSize: '14px' }}>{item.label}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );
      }

      case 'kanban': {
        // 从 dc 解构钩子
        const { useEffect, useMemo } = dc;
        const state = getKanbanState(component.id);
        const { editingCardId, editingColId } = state;
        // 使用全局右键菜单状态
        const contextMenu = kanbanContextMenu;

        // 看板组件使用缓存的样式
        const kanbanBaseStyle = getKanbanBaseStyle(component, baseStyle, comp);

        // 开始拖动卡片
        const handleCardMouseDown = (e, cardId, colId) => {
          if (!isEditing && !editingCardId) {
            e.preventDefault();
            e.stopPropagation();

            // 清理之前的克隆元素（如果有）
            const kds = getKanbanDragState(component.id);
            if (kds.cloneElement) {
              kds.cloneElement.remove();
              kds.cloneElement = null;
            }
            // 仅恢复当前看板组件内卡片的可见性
            const kanbanContainer = e.currentTarget.closest('[data-kanban-component-id]');
            if (kanbanContainer) {
              kanbanContainer.querySelectorAll('[data-kanban-card]').forEach(el => {
                el.style.visibility = 'visible';
              });
            }

            const rect = e.currentTarget.getBoundingClientRect();
            const card = (comp?.columns || []).find(c => c.id === colId)?.cards.find(c => c.id === cardId);

            if (!card) return;

            // 计算鼠标相对于卡片左上角的偏移
            dragState.offsetX = e.clientX - rect.left;
            dragState.offsetY = e.clientY - rect.top;

            // 创建简单的拖动占位符
            const placeholder = document.createElement('div');
            placeholder.style.cssText =
              "position: fixed;" +
              `left: ${rect.left}px;` +
              `top: ${rect.top}px;` +
              `width: ${rect.width}px;` +
              `min-height: ${rect.height}px;` +
              "z-index: 10000;" +
              "pointer-events: none;" +
              `background: ${tc('dragCloneBg')};` +
              "border-radius: 6px;" +
              `box-shadow: ${tc('dragCloneShadow')};` +
              "padding: 10px 12px;" +
              "font-size: 13px;" +
              `color: ${tc('textPrimary')};` +
              "overflow: hidden;" +
              "word-break: break-word;" +
              "box-sizing: border-box;" +
              "max-width: 100%;" +
              "white-space: pre-wrap;";
            placeholder.textContent = card.content || '';
            placeholder.id = 'kanban-dragging-clone';
            document.body.appendChild(placeholder);

            // 存储状态（按组件 ID 隔离），同时缓存 drop 所需上下文
            const kds2 = getKanbanDragState(component.id);
            kds2.draggingCardId = cardId;
            kds2.cloneElement = placeholder;
            kds2.sourceColId = colId;
            kds2.comp = comp;
            kds2.isEditing = isEditing;
            kds2.updateComponent = updateComponent;

            // 隐藏原卡片
            e.currentTarget.style.visibility = 'hidden';
          }
        };

        // 双击卡片进入编辑模式
        const handleCardDoubleClick = (e, cardId, colId) => {
          if (!isEditing) {
            e.stopPropagation();
            updateKanbanState(component.id, { editingCardId: cardId });
          }
        };

        // 双击列标题进入编辑模式
        const handleColumnTitleDoubleClick = (e, colId) => {
          if (!isEditing) {
            e.stopPropagation();
            updateKanbanState(component.id, { editingColId: colId });
          }
        };

        // 完成卡片编辑（失去焦点时保存）
        const handleCardEditBlur = (e, colId, cardId) => {
          updateCard(colId, cardId, e.target.value);
          updateKanbanState(component.id, { editingCardId: null });
        };

        // 卡片编辑键盘事件
        const handleCardEditKeyDown = (e, colId, cardId) => {
          if (e.key === 'Escape') {
            updateKanbanState(component.id, { editingCardId: null });
            e.stopPropagation();
          }
        };

        // 完成列标题编辑
        const handleColumnTitleEditBlur = (e, colId) => {
          updateColumnTitle(colId, e.target.value);
          updateKanbanState(component.id, { editingColId: null });
        };

        // 列标题键盘事件
        const handleColumnTitleEditKeyDown = (e, colId) => {
          if (e.key === 'Enter') {
            e.target.blur();
          } else if (e.key === 'Escape') {
            updateKanbanState(component.id, { editingColId: null });
            e.stopPropagation();
          }
        };

        // 右键菜单处理
        const handleContextMenu = (e, type, cardId = null, sourceColId = null) => {
          e.preventDefault();
          e.stopPropagation();

          // 直接使用 clientX/clientY，和卡片拖动保持一致
          setKanbanContextMenu({
            x: e.clientX,
            y: e.clientY,
            type,
            cardId,
            sourceColId,
            componentId: component.id
          });
        };

        // 看板拖放处理已移至主容器 onMouseUp，无需独立全局监听

        const addCard = (colId) => {
          const columns = comp?.columns || [];
          const newColumns = columns.map(col => {
            if (col.id === colId) {
              const newCard = {
                id: 'card' + Date.now(),
                content: '新卡片',
                backgroundColor: undefined
              };
              return {
                ...col,
                cards: [...col.cards, newCard]
              };
            }
            return col;
          });
          updateComponent(component.id, { columns: newColumns }, !isEditing);
        };

        const deleteCard = (colId, cardId) => {
          const columns = comp?.columns || [];
          const newColumns = columns.map(col => {
            if (col.id === colId) {
              return {
                ...col,
                cards: col.cards.filter(c => c.id !== cardId)
              };
            }
            return col;
          });
          updateComponent(component.id, { columns: newColumns }, !isEditing);
        };

        const updateCard = (colId, cardId, newContent) => {
          const columns = comp?.columns || [];
          const newColumns = columns.map(col => {
            if (col.id === colId) {
              return {
                ...col,
                cards: col.cards.map(c => c.id === cardId ? { ...c, content: newContent } : c)
              };
            }
            return col;
          });
          updateComponent(component.id, { columns: newColumns }, !isEditing);
        };

        const addColumn = () => {
          const columns = comp?.columns || [];
          const newColumn = {
            id: 'col' + Date.now(),
            title: '新列',
            cards: []
          };
          updateComponent(component.id, { columns: [...columns, newColumn] }, !isEditing);
        };

        const deleteColumn = (colId) => {
          const columns = comp?.columns || [];
          if (columns.length <= 1) return; // 至少保留一列
          updateComponent(component.id, { columns: columns.filter(col => col.id !== colId) }, !isEditing);
        };

        const updateColumnTitle = (colId, newTitle) => {
          const columns = comp?.columns || [];
          const newColumns = columns.map(col => {
            if (col.id === colId) {
              return { ...col, title: newTitle };
            }
            return col;
          });
          updateComponent(component.id, { columns: newColumns }, !isEditing);
        };

        return (
          <div style={kanbanBaseStyle} data-component-content="true" data-kanban-component-id={component.id}>
            {resizeHandles}
            {editButtons}
            <div style={{
              padding: '16px',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px'
            }}>
              {/* 标题行：标题 + 添加列按钮 - grid 叠加布局 */}
              {(comp?.showTitle !== false || (comp?.showAddColumnBtn !== false && !isEditing)) && (
                <div style={{
                  display: 'grid',
                  alignItems: 'center',
                  flexShrink: 0
                }}>
                  {comp?.showTitle !== false ? (
                    <span
                      dangerouslySetInnerHTML={{ __html: sanitizeHtml(comp?.title || '看板') }}
                      style={{ fontSize: '16px', fontWeight: '600', gridArea: '1 / 1', width: '100%' }}
                    />
                  ) : null}
                  {comp?.showAddColumnBtn !== false && !isEditing && (
                    <button
                      onClick={addColumn}
                      style={{
                        gridArea: '1 / 1',
                        justifySelf: 'end',
                        zIndex: 1,
                        padding: '4px 12px',
                        fontSize: '12px',
                        background: tc('accentBg'),
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = tc('accentBgHover')}
                      onMouseLeave={(e) => e.currentTarget.style.background = tc('accentBg')}
                    >
                      + 添加列
                    </button>
                  )}
                </div>
              )}

              {/* 看板列 */}
              <div
                style={{
                  display: 'flex',
                  gap: '12px',
                  alignItems: 'flex-start',
                  flexWrap: 'nowrap'
                }}
                onContextMenu={(e) => handleContextMenu(e, 'board')}
              >
                {(comp?.columns || []).map(column => (
                  <div
                    key={column.id}
                    data-column-id={column.id}
                    onContextMenu={(e) => handleContextMenu(e, 'column', null, column.id)}
                    style={{
                      minWidth: '200px',
                      maxWidth: '300px',
                      flex: '1 1 auto',
                      background: column.backgroundColor || tc('cardBgLight'),
                      borderRadius: '8px',
                      padding: '12px',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                      width: '100%'
                    }}
                  >
                    {/* 列标题 */}
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '8px',
                      fontWeight: '600',
                      fontSize: '13px',
                      flexShrink: 0
                    }}>
                      {(!isEditing && !editingColId) ? (
                        <span
                          onDoubleClick={(e) => handleColumnTitleDoubleClick(e, column.id)}
                          style={{ cursor: 'pointer', flex: 1 }}
                          title="双击编辑标题"
                        >
                          {column.title}
                        </span>
                      ) : (
                        <input
                          type="text"
                          defaultValue={column.title}
                          autoFocus={editingColId === column.id}
                          onBlur={(e) => {
                            if (editingColId === column.id) {
                              handleColumnTitleEditBlur(e, column.id);
                            } else if (isEditing) {
                              updateColumnTitle(column.id, e.target.value);
                            }
                          }}
                          onKeyDown={(e) => {
                            if (editingColId === column.id) {
                              handleColumnTitleEditKeyDown(e, column.id);
                            }
                          }}
                          onClick={(e) => e.stopPropagation()}
                          style={{
                            flex: 1,
                            padding: '2px 6px',
                            fontSize: '13px',
                            border: editingColId === column.id ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                            borderRadius: '4px',
                            background: tc('bgInput')
                          }}
                        />
                      )}
                      {!isEditing && (
                        <button
                          onClick={() => addCard(column.id)}
                          title="添加卡片"
                          style={{
                            width: '20px',
                            height: '20px',
                            borderRadius: '50%',
                            border: '1px solid rgba(102, 126, 234, 0.3)',
                            background: tc('accentSubtle'),
                            color: tc('accent'),
                            fontSize: '13px',
                            lineHeight: '20px',
                            cursor: 'pointer',
                            padding: 0,
                            flexShrink: 0,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.background = tc('accentBgHover')}
                          onMouseLeave={(e) => e.currentTarget.style.background = tc('accentSubtle')}
                        >
                          +
                        </button>
                      )}
                    </div>

                    {/* 卡片列表 */}
                    <div style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                      width: '100%',
                      minWidth: 0,
                      ...(comp?.maxHeight ? { maxHeight: comp.maxHeight, overflowY: 'auto' } : {})
                    }}>
                      {(column.cards || []).filter(c => c).map(card => {
                        const isEditingThisCard = editingCardId === card.id;
                        const cardBg = card.backgroundColor || tc('cardBgMedium');
                        return (
                          <div
                            key={card.id}
                            data-kanban-card={card.id}
                            onMouseDown={(e) => !isEditingThisCard && handleCardMouseDown(e, card.id, column.id)}
                            onDoubleClick={(e) => !isEditing && handleCardDoubleClick(e, card.id, column.id)}
                            onContextMenu={(e) => !isEditingThisCard && handleContextMenu(e, 'card', card.id, column.id)}
                            style={{
                              padding: '10px 12px',
                              background: cardBg,
                              borderRadius: '6px',
                              fontSize: '13px',
                              cursor: isEditing ? 'move' : (isEditingThisCard ? 'text' : 'grab'),
                              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                              transition: 'all 0.2s',
                              width: '100%',
                              maxWidth: '100%',
                              boxSizing: 'border-box',
                              wordBreak: 'break-word'
                            }}
                            onMouseEnter={(e) => {
                              if (!isEditing && !isEditingThisCard) {
                                e.currentTarget.style.boxShadow = '0 2px 6px rgba(0,0,0,0.15)';
                                e.currentTarget.style.transform = 'translateY(-1px)';
                              }
                            }}
                            onMouseLeave={(e) => {
                              if (!isEditing && !isEditingThisCard) {
                                e.currentTarget.style.background = cardBg;
                                e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
                                e.currentTarget.style.transform = 'translateY(0)';
                              }
                            }}
                          >
                            {isEditingThisCard ? (
                              <textarea
                                defaultValue={card.content}
                                autoFocus
                                onBlur={(e) => handleCardEditBlur(e, column.id, card.id)}
                                onKeyDown={(e) => handleCardEditKeyDown(e, column.id, card.id)}
                                onClick={(e) => e.stopPropagation()}
                                onMouseDown={(e) => e.stopPropagation()}
                                style={{
                                  width: '100%',
                                  minHeight: '60px',
                                  padding: '4px',
                                  fontSize: '13px',
                                  border: tc('kanbanEditBorder'),
                                  borderRadius: '4px',
                                  resize: 'none',
                                  background: tc('bgInput'),
                                  fontFamily: 'inherit',
                                  lineHeight: '1.4'
                                }}
                              />
                            ) : (
                              <div style={{ fontSize: '13px', color: tc('textPrimary'), lineHeight: '1.5', width: '100%', maxWidth: '100%', boxSizing: 'border-box', wordBreak: 'break-word' }}>
                                <Markdown content={card.content || ''} />
                              </div>
                            )}
                          </div>
                        );
                      })}
                  </div>
                </div>
                ))}
              </div>
            </div>
          </div>
        );
      }

      case 'image': {
        // 使用已定义的 ImageComponent，避免在 switch 中使用 hooks
        // ⚠️ 不能在这里使用 useState/useEffect 等 hooks
        // ImageComponent 已在文件开头定义，直接使用即可
        return (
          <ImageComponent
            key={component.id}
            component={component}
            comp={comp}
            isEditing={isEditing}
            baseStyle={baseStyle}
            resizeHandles={resizeHandles}
            editButtons={editButtons}
            vault={vault}
            openFile={openFile}
            commands={commands}
            onMouseDown={(e) => {
              if (!isEditing) return;
              const container = e.currentTarget;
              const rect = container.getBoundingClientRect();
              const componentScreenX = rect.left;
              const componentScreenY = rect.top;
              dragState.offsetX = e.clientX - componentScreenX;
              dragState.offsetY = e.clientY - componentScreenY;
              setDraggingId(comp.id);
            }}
          />
        );
      }

      case 'sidebar': {
        // 注入 CSS 给嵌入视图的 .view-content 加滚动条
        if (!document.getElementById('sidebar-view-scroll-style')) {
          const _s = document.createElement('style');
          _s.id = 'sidebar-view-scroll-style';
          _s.textContent = '[data-component-content] .workspace-leaf-content > .view-content { overflow-y: auto !important; }';
          document.head.appendChild(_s);
        }

        return <SidebarView dc={dc} app={app} comp={comp} baseStyle={baseStyle} resizeHandles={resizeHandles} editButtons={editButtons} contentContainerStyle={contentContainerStyle} />;
      }

      default:
        return <div style={baseStyle}>未知组件</div>;
    }
  };

  // 背景样式
  // 提取背景配置为独立的 useMemo，避免组件更新时触发背景重渲染
  const bgConfigMemo = useMemo(() => {
    return (tempConfig || config).background;
  }, [(tempConfig || config).background]);

  const backgroundStyle = useMemo(() => {
    const bgConfig = bgConfigMemo;

    if (bgConfig.type === 'image' && bgConfig.image) {
      // 转换图片路径为正确的 URL
      let imageUrl = bgConfig.image;

      // 如果是 Obsidian 附件路径，转换为资源路径
      if (!imageUrl.startsWith('http://') && !imageUrl.startsWith('https://')) {
        const file = vault.getAbstractFileByPath(imageUrl);
        if (file) {
          imageUrl = vault.getResourcePath(file);
        }
      }

      return {
        background: `url(${imageUrl}) center/cover no-repeat`
      };
    }
    return {
      background: bgConfig.value || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    };
  }, [bgConfigMemo]);

  // 获取视频 URL（使用缓存的背景配置）
  const getVideoUrl = () => {
    const bgConfig = bgConfigMemo;
    if (bgConfig.type === 'video' && bgConfig.video) {
      let videoUrl = bgConfig.video;
      // 如果是 Obsidian 附件路径，转换为资源路径
      if (!videoUrl.startsWith('http://') && !videoUrl.startsWith('https://')) {
        const file = vault.getAbstractFileByPath(videoUrl);
        if (file) {
          videoUrl = vault.getResourcePath(file);
        }
      }
      return videoUrl;
    }
    return null;
  };

  // 获取背景图片 URL（使用缓存的背景配置）
  const getBackgroundImageUrl = () => {
    const bgConfig = bgConfigMemo;
    if (bgConfig.type === 'image' && bgConfig.image) {
      let imageUrl = bgConfig.image;
      // 如果是 Obsidian 附件路径，转换为资源路径
      if (!imageUrl.startsWith('http://') && !imageUrl.startsWith('https://')) {
        const file = vault.getAbstractFileByPath(imageUrl);
        if (file) {
          imageUrl = vault.getResourcePath(file);
        }
      }
      return imageUrl;
    }
    return null;
  };

  // 当前使用的配置
  const currentConfig = tempConfig || config;

  // 入口页面（关闭后显示）内容
  const entryCardContent = (() => {
    const entryVideoUrl = getVideoUrl();
    return (
      <>
        {/* 视频背景 */}
        {bgConfigMemo.type === 'video' && entryVideoUrl && (() => {
          const videoFrostedBlur = bgConfigMemo?.videoFrostedBlur || 0;
          const videoFrostedOpacity = bgConfigMemo?.videoFrostedOpacity || 0;
          const videoBrightness = bgConfigMemo?.videoBrightness ?? 100;
          const videoContrast = bgConfigMemo?.videoContrast ?? 100;
          const videoOpacity = bgConfigMemo?.videoOpacity ?? 100;
          const videoSpeed = bgConfigMemo?.videoSpeed || 1;
          const videoFit = bgConfigMemo?.videoFit || 'cover';
          return (
            <>
              <video
                key={entryVideoUrl}
                ref={(el) => {
                  if (el) el.playbackRate = videoSpeed;
                }}
                autoPlay
                loop
                muted
                playsInline
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  objectFit: videoFit,
                  opacity: videoOpacity / 100,
                  filter: `brightness(${videoBrightness}%) contrast(${videoContrast}%)`,
                  zIndex: 0
                }}
              >
                <source src={entryVideoUrl} />
              </video>
              {/* 毛玻璃遮罩层 */}
              {(videoFrostedBlur > 0 || videoFrostedOpacity > 0) && (
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  zIndex: 1,
                  backdropFilter: `blur(${videoFrostedBlur}px)`,
                  WebkitBackdropFilter: `blur(${videoFrostedBlur}px)`,
                  background: `rgba(255, 255, 255, ${videoFrostedOpacity / 100})`,
                  pointerEvents: 'none'
                }} />
              )}
            </>
          );
        })()}

        {/* 图片背景 */}
        {bgConfigMemo.type === 'image' && (() => {
          const imageUrl = getBackgroundImageUrl();
          if (!imageUrl) return null;
          const imageFrostedBlur = bgConfigMemo?.imageFrostedBlur || 0;
          const imageFrostedOpacity = bgConfigMemo?.imageFrostedOpacity || 0;
          const imageBrightness = bgConfigMemo?.imageBrightness ?? 100;
          const imageContrast = bgConfigMemo?.imageContrast ?? 100;
          const imageOpacity = bgConfigMemo?.imageOpacity ?? 100;
          return (
            <>
              <img
                src={imageUrl}
                alt="背景"
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  opacity: imageOpacity / 100,
                  filter: `brightness(${imageBrightness}%) contrast(${imageContrast}%)`,
                  zIndex: 0
                }}
              />
              {(imageFrostedBlur > 0 || imageFrostedOpacity > 0) && (
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  zIndex: 1,
                  backdropFilter: `blur(${imageFrostedBlur}px)`,
                  WebkitBackdropFilter: `blur(${imageFrostedBlur}px)`,
                  background: `rgba(255, 255, 255, ${imageFrostedOpacity / 100})`,
                  pointerEvents: 'none'
                }} />
              )}
            </>
          );
        })()}

        {/* 半透明遮罩层（确保内容清晰可见） */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'rgba(0, 0, 0, 0.3)',
          zIndex: 2,
          pointerEvents: 'none'
        }} />

        {/* 内容卡片 */}
        <div style={{
          position: 'relative',
          zIndex: 3,
          padding: '40px',
          textAlign: 'center',
          background: 'transparent',
          borderRadius: '12px',
          color: '#fff',
          maxWidth: '400px',
          margin: '20px'
        }}>
          <div style={{ fontSize: '64px', marginBottom: '20px' }}>🏠</div>
          <h2 style={{
            margin: '0 0 20px 0',
            fontSize: '28px',
            fontWeight: '600',
            color: '#fff',
            textShadow: '0 2px 8px rgba(0,0,0,0.5)'
          }}>个人主页</h2>
          <p style={{
            margin: '0 0 30px 0',
            fontSize: '14px',
            color: 'rgba(255,255,255,0.9)',
            textShadow: '0 1px 4px rgba(0,0,0,0.5)'
          }}>
            点击下方按钮进入个人主页
          </p>
          <button
            onClick={() => setIsVisible(true)}
            style={{
              padding: '14px 32px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '16px',
              fontWeight: '500',
              boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.5)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
            }}
          >
            打开主页 →
          </button>
        </div>
      </>
    );
  })();

  // CSS 样式表：将固定样式提取为 CSS 类，减少内联样式对象创建
  const phCss = "[data-component-content]{padding:24px;background:" + tc('cardBgGlass') + ";box-shadow:" + tc('shadowGlass') + ";backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);overflow:hidden;display:flex;flex-direction:column;}" +
    ".ph-content{flex:1;overflow:hidden;display:flex;flex-direction:column;}" +
    ".ph-rs-t{position:absolute;top:-8px;left:0;right:0;height:16px;cursor:ns-resize;z-index:10;}" +
    ".ph-rs-b{position:absolute;bottom:-8px;left:0;right:0;height:16px;cursor:ns-resize;z-index:10;}" +
    ".ph-rs-l{position:absolute;left:-8px;top:0;bottom:0;width:16px;cursor:ew-resize;z-index:10;}" +
    ".ph-rs-r{position:absolute;right:-8px;top:0;bottom:0;width:16px;cursor:ew-resize;z-index:10;}" +
    ".ph-rs-br{position:absolute;bottom:-10px;right:-10px;width:32px;height:32px;cursor:nwse-resize;border-radius:0 0 0 8px;z-index:11;background:linear-gradient(135deg,transparent 50%," + tc('accent') + " 50%);}" +
    ".ph-eb-wrap{position:absolute;top:8px;right:8px;display:flex;gap:5px;z-index:10;}" +
    ".ph-eb-btn{width:24px;height:24px;border-radius:50%;background:" + tc('editBtnBg') + ";border:" + tc('editBtnBorder') + ";backdrop-filter:blur(4px);color:#fff;font-size:11px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:" + tc('shadowGlassSmall') + ";transition:all 0.2s;padding:0;}" +
    ".ph-eb-del{font-size:13px;font-weight:300;}" +
    ".ph-guide-v{position:absolute;top:0;height:100%;width:1px;background:#ff6b6b;}" +
    ".ph-guide-h{position:absolute;left:0;width:100%;height:1px;background:#ff6b6b;}" +
    ".ph-guide-ct{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99999;}" +
    ".ph-grid-cv{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;}" +
    ".ph-bg-dim{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.3);z-index:0;}" +
    ".ph-comp-wrap{position:absolute;}";

  return (
    <div
      ref={rootContainerRef}
      data-homepage-root="true"
      style={isVisible ? {
        position: 'absolute',
        left: 0,
        top: 0,
        width: '100%',
        height: '100%',
        ...backgroundStyle,
        zIndex: 9999,
        display: 'flex',
        flexDirection: 'column',
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        overflowX: 'auto',
        overflowY: 'hidden'
      } : {
        position: 'relative',
        minHeight: '400px',
        ...backgroundStyle,
        borderRadius: '12px',
        overflow: 'hidden',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif'
      }}
      onMouseMove={isVisible ? (e) => {
        handleDragMove(e);
        handleResizeMove(e);
        handleMarkdownCardDragMove(e);
        handleMarkdownCardResizeMove(e);

        // 看板卡片拖动 - 直接更新所有活跃看板的克隆元素位置
        dragState.kanbanDragStates.forEach((state) => {
          if (state.cloneElement) {
            state.cloneElement.style.left = (e.clientX - dragState.offsetX) + 'px';
            state.cloneElement.style.top = (e.clientY - dragState.offsetY) + 'px';
          }
        });
      } : undefined}
      onMouseUp={isVisible ? (e) => {
        handleDragEnd(e);
        handleMarkdownCardDragEnd();
        handleKanbanDrop(e);
      } : undefined}
      onClick={(e) => {
        // 处理 Markdown 卡片中双链的点击跳转
        // 容器被移到 view-content 后，Obsidian 的事件代理无法触达内部链接，需手动处理
        if (isEditing) return;
        const target = e.target.closest('a');
        if (!target) return;
        const href = target.getAttribute('href') || target.getAttribute('data-href');
        if (!href) return;
        // 只处理内部链接（wiki 链接，通常不以 http 开头）
        if (href.startsWith('http://') || href.startsWith('https://') || href.startsWith('#')) return;
        e.preventDefault();
        e.stopPropagation();
        // 使用 data-href（原始 vault 路径），openLinkText 会自动处理路径解析、#标题、别名等
        const linkPath = target.getAttribute('data-href') || href;
        const destName = decodeURIComponent(linkPath);
        if (!destName) return;
        if (e.ctrlKey || e.metaKey) {
          // Ctrl+点击：新标签页打开
          workspace.openLinkText(destName, currentFilePath, 'tab');
        } else {
          // 普通点击：当前标签页打开，先关闭主页再导航
          setIsVisible(false);
          setShowAuxGridSettings(false);
          setAuxGrid(prev => ({ ...prev, show: false }));
          setTimeout(() => {
            workspace.openLinkText(destName, currentFilePath, false);
          }, 50);
        }
      }}
    >
      <style>{phCss}</style>
      {/* 入口卡片（关闭后显示） */}
      {!isVisible && entryCardContent}
      {/* 全屏主页内容 */}
      {isVisible && <>
      <style>{ "[data-homepage-root] { color: #333 !important; }" +
        "[data-homepage-root] input:not([type=\"radio\"]):not([type=\"checkbox\"]), [data-homepage-root] select, [data-homepage-root] textarea {" +
        "  background-color: #fff !important; color: #333 !important;" +
        "  caret-color: #333 !important; -webkit-text-fill-color: #333 !important;" +
        "}" +
        "[data-homepage-root] select option { background-color: #fff !important; color: #333 !important; }" +
        "[data-homepage-root] input::placeholder, [data-homepage-root] textarea::placeholder {" +
        "  color: #999 !important; -webkit-text-fill-color: #999 !important;" +
        "}" +
        "[data-homepage-root] [contenteditable=\"true\"] {" +
        "  caret-color: #333 !important; color: #333 !important; -webkit-text-fill-color: #333 !important;" +
        "}" +
        "[data-homepage-root] .markdown-card-content," +
        "[data-homepage-root] .markdown-card-content p," +
        "[data-homepage-root] .markdown-card-content span," +
        "[data-homepage-root] .markdown-card-content div," +
        "[data-homepage-root] .markdown-card-content li," +
        "[data-homepage-root] .markdown-card-content h1," +
        "[data-homepage-root] .markdown-card-content h2," +
        "[data-homepage-root] .markdown-card-content h3," +
        "[data-homepage-root] .markdown-card-content h4," +
        "[data-homepage-root] .markdown-card-content h5," +
        "[data-homepage-root] .markdown-card-content h6," +
        "[data-homepage-root] .markdown-card-content strong," +
        "[data-homepage-root] .markdown-card-content em," +
        "[data-homepage-root] .markdown-card-content blockquote {" +
        "  color: inherit !important; -webkit-text-fill-color: inherit !important;" +
        "}" +
        "[data-homepage-root] a, [data-homepage-root] .internal-link, [data-homepage-root] .external-link, [data-homepage-root] .cm-link {" +
        "  color: #667eea !important; -webkit-text-fill-color: #667eea !important;" +
        "}" +
        "[data-homepage-root] svg.svg-icon { color: inherit !important; fill: none !important; stroke: currentColor !important; }" +
        "[data-homepage-root] .is-live-preview .cm-line, [data-homepage-root] .cm-content { caret-color: #333 !important; }" +
        "[data-homepage-root] .workspace-split * {" +
        "  color: revert !important; -webkit-text-fill-color: revert !important; caret-color: revert !important;" +
        "}" +
        "[data-homepage-root] .workspace-split input," +
        "[data-homepage-root] .workspace-split select," +
        "[data-homepage-root] .workspace-split textarea," +
        "[data-homepage-root] .workspace-split select option {" +
        "  background-color: revert !important; color: revert !important;" +
        "  caret-color: revert !important; -webkit-text-fill-color: revert !important;" +
        "}" +
        "[data-page-settings] { background-color: #fff !important; color: #333 !important; }" +
        "[data-page-settings] button { color: #333 !important; }" +
        "[data-page-settings] button:hover { background-color: rgba(0,0,0,0.08) !important; }" +
        "[data-page-settings] input, [data-page-settings] select, [data-page-settings] textarea {" +
        "  background-color: #fff !important; color: #333 !important; border-color: #ddd !important;" +
        "}" +
        "[data-page-settings] input::placeholder { color: #999 !important; }" +
        "[data-page-settings] .text-secondary { color: #666 !important; }" +
        "[data-page-settings] .text-label { color: #999 !important; }" +
        "[data-page-settings] .border-subtle { border-color: #f0f0f0 !important; }" +
        "[data-page-settings] .border-input { border-color: #ddd !important; }" +
        "[data-homepage-root] ::-webkit-scrollbar { width: 8px; height: 8px; }" +
        "[data-homepage-root] ::-webkit-scrollbar-track { background: transparent; }" +
        "[data-homepage-root] ::-webkit-scrollbar-thumb { background: rgba(0, 0, 0, 0.2); border-radius: 4px; }" +
        "[data-homepage-root] ::-webkit-scrollbar-thumb:hover { background: rgba(0, 0, 0, 0.3); }" +
        "[data-homepage-root] ::-webkit-scrollbar-thumb:active { background: rgba(0, 0, 0, 0.35); }" +
        "[data-homepage-root] { scrollbar-width: thin; scrollbar-color: rgba(0, 0, 0, 0.2) transparent; }" }</style>
      {/* 视频背景 */}
      {bgConfigMemo.type === 'video' && (() => {
        const videoUrl = getVideoUrl();
        if (!videoUrl) return null;
        const videoFrostedBlur = bgConfigMemo?.videoFrostedBlur || 0;
        const videoFrostedOpacity = bgConfigMemo?.videoFrostedOpacity || 0;
        const videoBrightness = bgConfigMemo?.videoBrightness ?? 100;
        const videoContrast = bgConfigMemo?.videoContrast ?? 100;
        const videoOpacity = bgConfigMemo?.videoOpacity ?? 100;
        const videoSpeed = bgConfigMemo?.videoSpeed || 1;
        const videoFit = bgConfigMemo?.videoFit || 'cover';
        return (
          <>
            <video
              key={videoUrl}
              ref={(el) => {
                if (el) el.playbackRate = videoSpeed;
              }}
              autoPlay
              loop
              muted
              playsInline
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                objectFit: videoFit,
                opacity: videoOpacity / 100,
                filter: `brightness(${videoBrightness}%) contrast(${videoContrast}%)`,
                zIndex: -1
              }}
            >
              <source src={videoUrl} />
            </video>
            {/* 毛玻璃遮罩层 */}
            {(videoFrostedBlur > 0 || videoFrostedOpacity > 0) && (
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                zIndex: -1,
                backdropFilter: `blur(${videoFrostedBlur}px)`,
                WebkitBackdropFilter: `blur(${videoFrostedBlur}px)`,
                background: `rgba(255, 255, 255, ${videoFrostedOpacity / 100})`,
                pointerEvents: 'none'
              }} />
            )}
          </>
        );
      })()}

      {/* 辅助网格 - Canvas 绘制，仅 1 个 DOM 节点 */}
      {auxGrid.show && (
        <canvas ref={gridCanvasRef} className="ph-grid-cv" />
      )}

      {/* 背景遮罩（图片或视频模式时） */}
      {(bgConfigMemo.type === 'image' || bgConfigMemo.type === 'video') && (
        <div className="ph-bg-dim" />
      )}

      {/* 顶部按钮区 */}
      <div style={{
        position: 'absolute',
        top: '16px',
        right: '16px',
        zIndex: 10000,
        display: 'flex',
        gap: '12px',
        alignItems: 'center'
      }}>
        {!isEditing ? (
          <>
            <div
              style={{ position: 'relative' }}
              onMouseEnter={() => {
                if (menuCollapseTimer.current) {
                  clearTimeout(menuCollapseTimer.current);
                  menuCollapseTimer.current = null;
                }
                setMenuExpanded(true);
              }}
              onMouseLeave={() => {
                if (!menuPin) {
                  menuCollapseTimer.current = setTimeout(() => {
                    setMenuExpanded(false);
                  }, 3000);
                }
              }}
              onClick={() => {
                if (menuPin) {
                  setMenuPin(false);
                  setMenuExpanded(false);
                } else {
                  setMenuPin(true);
                  setMenuExpanded(true);
                }
              }}
            >
              <button
                style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'rgba(0, 0, 0, 0.3)',
                  border: 'none',
                  color: '#fff',
                  fontSize: '16px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(0, 0, 0, 0.5)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(0, 0, 0, 0.3)'}
              >
                <dc.Icon icon="menu" />
              </button>
              <div style={{
                position: 'absolute',
                top: 0,
                right: '40px',
                display: 'flex',
                gap: '8px',
                transition: 'opacity 0.2s, transform 0.2s',
                opacity: menuExpanded ? 1 : 0,
                transform: menuExpanded ? 'translateX(0)' : 'translateX(8px)',
                pointerEvents: menuExpanded ? 'auto' : 'none'
              }}>
                <button
                  onClick={startEditing}
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    background: 'rgba(0, 0, 0, 0.3)',
                    border: 'none',
                    color: '#fff',
                    fontSize: '16px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                  title="编辑"
                ><dc.Icon icon="settings" /></button>
                <button
                  onClick={() => {
                    setIsVisible(false);
                    setShowAuxGridSettings(false);
                    setAuxGrid(prev => ({ ...prev, show: false }));
                  }}
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    background: 'rgba(0, 0, 0, 0.3)',
                    border: 'none',
                    color: '#fff',
                    fontSize: '20px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                  title="关闭"
                >×</button>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* 查看模式下的统一尺寸按钮 */}
            {viewMode && (
              <button
                onClick={unifyMarkdownCardSizes}
                style={{
                  padding: '10px 16px',
                  background: tc('accentBgHover'),
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(102, 126, 234, 0.5)',
                  borderRadius: '20px',
                  color: '#fff',
                  fontSize: '13px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = tc('accentBgHover')}
                onMouseLeave={(e) => e.currentTarget.style.background = tc('accentBgHover')}
              >
                📐 统一尺寸
              </button>
            )}

            {/* 辅助网格按钮 */}
            <button
              ref={auxGridButtonRef}
              onClick={() => {
                const newState = !showAuxGridSettings;
                setShowAuxGridSettings(newState);
                if (newState) {
                  const rect = auxGridButtonRef.current.getBoundingClientRect();
                  setAuxGridSettingsPos({
                    right: window.innerWidth - rect.right,
                    top: rect.bottom + 8
                  });
                }
              }}
              style={{
                padding: '10px 16px',
                background: 'rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '20px',
                color: '#fff',
                fontSize: '13px',
                cursor: 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                gap: '10px'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = tc('accentBgHover')}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'}
            >
              网格
              <div
                onClick={(e) => {
                  e.stopPropagation();
                  setAuxGrid(prev => ({ ...prev, show: !prev.show }));
                }}
                style={{
                  position: 'relative',
                  width: '36px',
                  height: '18px',
                  background: auxGrid.show ? 'rgba(102, 126, 234, 0.9)' : 'rgba(255, 255, 255, 0.3)',
                  borderRadius: '9px',
                  cursor: 'pointer',
                  transition: 'background 0.2s'
                }}
              >
                <div style={{
                  position: 'absolute',
                  left: auxGrid.show ? '19px' : '1px',
                  top: '1px',
                  width: '16px',
                  height: '16px',
                  background: '#fff',
                  borderRadius: '8px',
                  transition: 'left 0.2s',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.2)'
                }} />
              </div>
            </button>

            {/* 辅助网格设置菜单 */}
            {showAuxGridSettings && (
              <div
                onContextMenu={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                }}
                style={{
                  position: 'fixed',
                  right: auxGridSettingsPos.right + 'px',
                  top: auxGridSettingsPos.top + 'px',
                  width: '240px',
                  background: 'rgba(255, 255, 255, 0.98)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(0, 0, 0, 0.1)',
                  borderRadius: '12px',
                  padding: '16px',
                  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
                  zIndex: 10001
                }}
              >
                <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '12px', color: tc('textPrimary') }}>辅助网格设置</div>
                <div style={{ marginBottom: '12px' }}>
                  <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>网格线颜色</label>
                  <input
                    type="color"
                    value={auxGrid.lineColor}
                    onChange={(e) => setAuxGrid(prev => ({ ...prev, lineColor: e.target.value }))}
                    onClick={(e) => e.stopPropagation()}
                    style={{
                      width: '100%',
                      height: '36px',
                      border: tc('borderInput'),
                      borderRadius: '6px',
                      cursor: 'pointer',
                      padding: '2px'
                    }}
                  />
                </div>
                <div style={{ marginBottom: '12px' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={auxGrid.showHorizontal}
                      onChange={(e) => setAuxGrid(prev => ({ ...prev, showHorizontal: e.target.checked }))}
                      onClick={(e) => e.stopPropagation()}
                      style={{ cursor: 'pointer' }}
                    />
                    显示水平线
                  </label>
                  <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '4px' }}>水平线密度: {auxGrid.horizontalDensity}px</label>
                  <input
                    type="range"
                    min="10"
                    max="200"
                    step="5"
                    value={auxGrid.horizontalDensity}
                    onChange={(e) => setAuxGrid(prev => ({ ...prev, horizontalDensity: parseInt(e.target.value) }))}
                    onClick={(e) => e.stopPropagation()}
                    style={{
                      width: '100%',
                      cursor: 'pointer'
                    }}
                  />
                </div>
                <div style={{ marginBottom: '12px' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={auxGrid.showVertical}
                      onChange={(e) => setAuxGrid(prev => ({ ...prev, showVertical: e.target.checked }))}
                      onClick={(e) => e.stopPropagation()}
                      style={{ cursor: 'pointer' }}
                    />
                    显示垂直线
                  </label>
                  <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '4px' }}>垂直线密度: {auxGrid.verticalDensity}px</label>
                  <input
                    type="range"
                    min="10"
                    max="200"
                    step="5"
                    value={auxGrid.verticalDensity}
                    onChange={(e) => setAuxGrid(prev => ({ ...prev, verticalDensity: parseInt(e.target.value) }))}
                    onClick={(e) => e.stopPropagation()}
                    style={{
                      width: '100%',
                      cursor: 'pointer'
                    }}
                  />
                </div>
                <div style={{ marginBottom: '12px' }}>
                  <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>线条宽度: {auxGrid.lineWidth}px</label>
                  <input
                    type="range"
                    min="1"
                    max="3"
                    step="0.5"
                    value={auxGrid.lineWidth}
                    onChange={(e) => setAuxGrid(prev => ({ ...prev, lineWidth: parseFloat(e.target.value) }))}
                    onClick={(e) => e.stopPropagation()}
                    style={{
                      width: '100%',
                      cursor: 'pointer'
                    }}
                  />
                </div>
              </div>
            )}

            {/* 页面设置按钮 */}
            <button
              onClick={() => {
                const newState = !showPageSettings;
                if (newState && !isEditing) {
                  // 打开页面设置时自动进入编辑模式
                  startEditing();
                }
                setShowPageSettings(newState);
              }}
              style={{
                padding: '10px 16px',
                background: showPageSettings ? tc('accentBgHover') : 'rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '20px',
                color: '#fff',
                fontSize: '13px',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = tc('cardBgLight')}
              onMouseLeave={(e) => e.currentTarget.style.background = tc('cardBgSubtle')}
            >
              页面设置
            </button>

            {/* 取消按钮 */}
            <button
              onClick={cancelEditing}
              style={{
                padding: '10px 16px',
                background: 'rgba(245, 87, 108, 0.3)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(245, 87, 108, 0.5)',
                borderRadius: '20px',
                color: '#fff',
                fontSize: '13px',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(245, 87, 108, 0.5)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(245, 87, 108, 0.3)'}
            >
              ✕ 取消
            </button>

            {/* 保存按钮 */}
            <button
              onClick={saveAndExit}
              style={{
                padding: '10px 16px',
                background: 'rgba(72, 187, 120, 0.3)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(72, 187, 120, 0.5)',
                borderRadius: '20px',
                color: '#fff',
                fontSize: '13px',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(72, 187, 120, 0.5)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(72, 187, 120, 0.3)'}
            >
              ✓ 保存
            </button>
          </>
        )}
      </div>

      {/* 页面设置面板 */}
      {isEditing && showPageSettings && (
        <div
          data-page-settings="true"
          style={{
            position: 'absolute',
            right: pageSettingsPos.right + 'px',
            top: pageSettingsPos.top + 'px',
            width: pageSettingsWidth + 'px',
            background: tc('cardBg'),
            backdropFilter: 'blur(10px)',
            borderRadius: '16px',
            boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
            padding: '16px',
            zIndex: 10000,
            maxHeight: 'calc(100% - 100px)',
            overflowY: 'auto'
          }}>
          {/* 拖动条 */}
          <div
            onMouseDown={(e) => handleSettingsMouseDown(e, 'drag')}
            style={{
              height: '24px',
              marginBottom: '8px',
              cursor: 'move',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              opacity: 0.5
            }}
            onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
            onMouseLeave={(e) => e.currentTarget.style.opacity = '0.5'}
          >
            <div style={{ width: '40px', height: '4px', background: '#ccc', borderRadius: '2px' }} />
          </div>

          {/* 调整大小手柄 */}
          <div
            onMouseDown={(e) => {
              e.preventDefault();
              e.stopPropagation();
              handleSettingsMouseDown(e, 'resize');
            }}
            style={{
              position: 'absolute',
              right: '-6px',
              top: '0',
              bottom: '0',
              width: '12px',
              cursor: 'ew-resize',
              zIndex: 10
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = tc('accentBgHover')}
            onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
          />

          {/* 标题栏 */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>页面设置</h3>
            <button
              onClick={() => setShowPageSettings(false)}
              style={{
                width: '24px',
                height: '24px',
                borderRadius: '4px',
                background: 'transparent',
                border: 'none',
                color: tc('textLabel'),
                fontSize: '18px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 0
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(0,0,0,0.05)';
                e.currentTarget.style.color = '#333';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = tc('textLabel');
              }}
            >
              ×
            </button>
          </div>

          {/* 背景设置 */}
          <div style={{ marginBottom: '16px' }}>
            <div 
              onClick={() => setShowBackgroundSettings(!showBackgroundSettings)}
              style={{ 
                fontSize: '13px', 
                color: tc('textSecondary'), 
                marginBottom: showBackgroundSettings ? '8px' : '0',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '8px 0',
                userSelect: 'none'
              }}
            >
              <span>背景设置</span>
              <span style={{ 
                fontSize: '10px', 
                transition: 'transform 0.2s',
                transform: showBackgroundSettings ? 'rotate(180deg)' : 'rotate(0deg)'
              }}>▼</span>
            </div>
            {showBackgroundSettings && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {/* 预设背景按钮 */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
                  {/* 时尚配色风格 */}
                  <button
                    onClick={() => setBackground('gradient', 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)')}
                    style={{
                      padding: '12px 8px',
                      background: 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '11px',
                      cursor: 'pointer',
                      textShadow: '0 1px 2px rgba(0,0,0,0.3)',
                      boxShadow: '0 2px 8px rgba(255,107,107,0.3)'
                    }}
                  >
                    时尚活力
                  </button>
                  {/* 少女粉红风格 */}
                  <button
                    onClick={() => setBackground('gradient', 'linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%)')}
                    style={{
                      padding: '12px 8px',
                      background: 'linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%)',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '11px',
                      cursor: 'pointer',
                      textShadow: '0 1px 2px rgba(0,0,0,0.2)',
                      boxShadow: '0 2px 8px rgba(255,117,140,0.4)'
                    }}
                  >
                    少女粉红
                  </button>
                  {/* 自然清新风格 */}
                  <button
                    onClick={() => setBackground('gradient', 'linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)')}
                    style={{
                      padding: '12px 8px',
                      background: 'linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '11px',
                      cursor: 'pointer',
                      textShadow: '0 1px 2px rgba(0,0,0,0.3)',
                      boxShadow: '0 2px 8px rgba(86,171,47,0.3)'
                    }}
                  >
                    自然清新
                  </button>
                  {/* 晴空蔚蓝风格 */}
                  <button
                    onClick={() => setBackground('gradient', 'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)')}
                    style={{
                      padding: '12px 8px',
                      background: 'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '11px',
                      cursor: 'pointer',
                      textShadow: '0 1px 2px rgba(0,0,0,0.2)',
                      boxShadow: '0 2px 8px rgba(102,166,255,0.4)'
                    }}
                  >
                    晴空蔚蓝
                  </button>
                  {/* 暗夜极光风格 */}
                  <button
                    onClick={() => setBackground('gradient', 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)')}
                    style={{
                      padding: '12px 8px',
                      background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '11px',
                      cursor: 'pointer',
                      textShadow: '0 1px 2px rgba(0,0,0,0.5)',
                      boxShadow: '0 2px 8px rgba(48,43,99,0.4)'
                    }}
                  >
                    暗夜极光
                  </button>
                  {/* 梦幻粉彩风格 */}
                  <button
                    onClick={() => setBackground('gradient', 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)')}
                    style={{
                      padding: '12px 8px',
                      background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
                      border: 'none',
                      borderRadius: '8px',
                      color: tc('textPrimary'),
                      fontSize: '11px',
                      cursor: 'pointer',
                      textShadow: '0 1px 2px rgba(255,255,255,0.5)',
                      boxShadow: '0 2px 8px rgba(252,182,159,0.3)'
                    }}
                  >
                    梦幻粉彩
                  </button>
                </div>
                
                {/* 自定义颜色调色板 */}
                <div style={{
                  padding: '12px',
                  background: tc('bgPanel'),
                  borderRadius: '8px',
                  border: '1px dashed #ddd'
                }}>
                  <div style={{ fontSize: '11px', color: tc('textSecondary'), marginBottom: '8px', fontWeight: '500' }}>
                    自定义调色板
                  </div>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '8px' }}>
                    <input
                      id="custom-color-1"
                      type="color"
                      defaultValue="#667eea"
                      style={{
                        width: '40px',
                        height: '36px',
                        border: tc('borderInput'),
                        borderRadius: '6px',
                        cursor: 'pointer',
                        padding: '2px'
                      }}
                    />
                    <span style={{ fontSize: '12px', color: tc('textLabel') }}>→</span>
                    <input
                      id="custom-color-2"
                      type="color"
                      defaultValue="#764ba2"
                      style={{
                        width: '40px',
                        height: '36px',
                        border: tc('borderInput'),
                        borderRadius: '6px',
                        cursor: 'pointer',
                        padding: '2px'
                      }}
                    />
                    <div style={{ flex: 1, display: 'flex', gap: '4px' }}>
                      <button
                        onClick={() => {
                          const color1 = document.getElementById('custom-color-1')?.value || '#667eea';
                          setBackground('solid', color1);
                        }}
                        style={{
                          flex: 1,
                          padding: '8px 4px',
                          background: tc('bgInput'),
                          border: tc('borderInput'),
                          borderRadius: '6px',
                          fontSize: '11px',
                          cursor: 'pointer',
                          color: tc('textPrimary')
                        }}
                      >
                        纯色
                      </button>
                      <button
                        onClick={() => {
                          const color1 = document.getElementById('custom-color-1')?.value || '#667eea';
                          const color2 = document.getElementById('custom-color-2')?.value || '#764ba2';
                          setBackground('gradient', `linear-gradient(135deg, ${color1} 0%, ${color2} 100%)`);
                        }}
                        style={{
                          flex: 1,
                          padding: '8px 4px',
                          background: '#667eea',
                          border: 'none',
                          borderRadius: '6px',
                          fontSize: '11px',
                          cursor: 'pointer',
                          color: '#fff'
                        }}
                      >
                        渐变
                      </button>
                    </div>
                  </div>
                  {/* 快速颜色选择 */}
                  <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                    {['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#1dd1a1', '#ff9f43', '#ee5a24', '#c8d6e5', '#222f3e'].map(color => (
                      <div
                        key={color}
                        onClick={() => {
                          const color1El = document.getElementById('custom-color-1');
                          if (color1El) color1El.value = color;
                        }}
                        style={{
                          width: '24px',
                          height: '24px',
                          background: color,
                          borderRadius: '4px',
                          cursor: 'pointer',
                          border: '2px solid transparent',
                          transition: 'all 0.2s'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = 'scale(1.15)';
                          e.currentTarget.style.borderColor = '#667eea';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = 'scale(1)';
                          e.currentTarget.style.borderColor = 'transparent';
                        }}
                        title={color}
                      />
                    ))}
                  </div>
                </div>

                {/* 图片背景设置 */}
                <div style={{ display: 'flex', gap: '8px' }}>
                  <div style={{ flex: 1, position: 'relative' }}>
                    {(() => {
                      // 验证图片 URL 是否有效
                      const validateImageUrl = (url, onSuccess) => {
                        setBgUrlError('');

                        // 创建图片对象进行检测
                        const img = new Image();

                        // 成功加载
                        img.onload = () => {
                          setBgUrlError('');
                          onSuccess();
                        };

                        // 加载失败
                        img.onerror = () => {
                          setBgUrlError('图片地址不正确');
                        };

                        // 开始加载
                        img.src = url;
                      };

                      // 提取图片搜索逻辑为函数，避免代码重复
                      const searchImages = (searchTerm) => {
                        const dropdown = document.getElementById('page-bg-dropdown');
                        const list = document.getElementById('page-bg-list');

                        if (!dropdown || !list) return;

                        if (searchTerm.length === 0) {
                          dropdown.style.display = 'none';
                          return;
                        }

                        list.innerHTML = '';

                        // 检查是否是 http/https URL
                        if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                          // URL 模式：在下拉列表中显示该 URL
                          const item = document.createElement('div');
                          item.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; color: #667eea; font-weight: 500;";
                          item.textContent = searchTerm;
                          item.onmousedown = (e) => {
                            e.preventDefault();
                            setBgUrlError('');
                            // 点击后进行检测
                            validateImageUrl(searchTerm, () => {
                              setBackground('image', searchTerm);
                            });
                            dropdown.style.display = 'none';
                          };
                          list.appendChild(item);
                          dropdown.style.display = 'block';
                          return;
                        }

                        // 本地文件搜索模式
                        // 获取所有图片文件
                        const allFiles = vault.getFiles();
                        const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico', '.avif', '.tiff', '.tif', '.heic', '.heif'];
                        const imageFiles = allFiles.filter(f =>
                          imageExtensions.some(ext => f.path.toLowerCase().endsWith(ext))
                        );

                        // 模糊匹配
                        const matches = imageFiles.filter(f =>
                          f.path.toLowerCase().includes(searchTerm)
                        ).slice(0, 10);

                        if (matches.length === 0) {
                          const noResult = document.createElement('div');
                          noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                          noResult.textContent = '未找到匹配的图片';
                          list.appendChild(noResult);
                        } else {
                          matches.forEach(match => {
                            const item = document.createElement('div');
                            item.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #f0f0f0;";
                            item.textContent = match.path;
                            item.onmousedown = (e) => {
                              e.preventDefault();
                              const inputEl = document.getElementById('page-bg-input');
                              if (inputEl) {
                                inputEl.value = match.path;
                              }
                              setBgUrlError('');
                              setBackground('image', match.path);
                              dropdown.style.display = 'none';
                            };
                            list.appendChild(item);
                          });

                          dropdown.style.display = 'block';
                        }
                      };

                      return (
                        <>
                        <input
                          id="page-bg-input"
                          type="text"
                          placeholder="输入图片路径或 URL"
                          defaultValue={(tempConfig || config).background?.type === 'image' ? (tempConfig || config).background?.value : ''}
                          onClick={(e) => e.stopPropagation()}
                          onFocus={() => {
                            const dropdown = document.getElementById('page-bg-dropdown');
                            if (dropdown) dropdown.style.display = 'block';
                            setBgUrlError('');
                          }}
                          onBlur={(e) => {
                            setTimeout(() => {
                              const dropdown = document.getElementById('page-bg-dropdown');
                              if (dropdown) dropdown.style.display = 'none';
                            }, 200);
                          }}
                          onKeyDown={(e) => {
                            // 回车键确认
                            if (e.key === 'Enter') {
                              const url = e.target.value.trim();
                              if (url) {
                                if (url.startsWith('http://') || url.startsWith('https://')) {
                                  // URL 模式：先检测再应用
                                  setBgUrlError('');
                                  validateImageUrl(url, () => {
                                    setBackground('image', url);
                                  });
                                } else {
                                  // 本地路径模式：直接应用
                                  setBgUrlError('');
                                  setBackground('image', url);
                                }
                              }
                              e.currentTarget.blur();
                            }
                          }}
                          onCompositionStart={(e) => {
                            e.target.dataset.isComposing = 'true';
                          }}
                          onCompositionEnd={(e) => {
                            e.target.dataset.isComposing = 'false';
                            // 输入法结束后触发一次搜索
                            const url = e.target.value.trim();
                            if (url) {
                              searchImages(url.toLowerCase());
                            }
                          }}
                          onInput={(e) => {
                            const url = e.target.value.trim();
                            // 中文输入法输入过程中不执行搜索
                            if (e.target.dataset.isComposing === 'true') return;

                            searchImages(url.toLowerCase());
                          }}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '8px',
                            fontSize: '12px'
                          }}
                        />
                        {bgUrlError && (
                          <div style={{
                            color: tc('errorText'),
                            fontSize: '11px',
                            marginTop: '4px'
                          }}>
                            {bgUrlError}
                          </div>
                        )}
                        </>
                      );
                    })()}
                    {/* 搜索结果下拉框 */}
                    <div
                      id="page-bg-dropdown"
                      style={{
                        display: 'none',
                        position: 'absolute',
                        top: '100%',
                        left: 0,
                        right: 0,
                        background: tc('bgInput'),
                        border: tc('borderInput'),
                        borderRadius: '6px',
                        boxShadow: tc('shadowPopup'),
                        zIndex: 100,
                        maxHeight: '200px',
                        overflowY: 'auto',
                        marginTop: '4px'
                      }}
                    >
                      <div id="page-bg-list"></div>
                    </div>
                  </div>

                  {/* 上传按钮 */}
                  <button
                    onClick={() => {
                      const input = document.createElement('input');
                      input.type = 'file';
                      input.accept = 'image/*';
                      input.onchange = async (e) => {
                        const file = e.target.files?.[0];
                        if (!file) return;

                        try {
                          // 生成唯一文件名
                          const timestamp = Date.now();
                          const ext = file.name.split('.').pop() || 'png';
                          const fileName = `bg_${timestamp}.${ext}`;

                          // 使用 Obsidian API 获取附件保存路径（根据用户设置的附件默认存放路径）
                          const filePath = await app.fileManager.getAvailablePathForAttachment(fileName, currentFilePath);

                          // 读取文件内容
                          const arrayBuffer = await file.arrayBuffer();

                          // 创建文件
                          await vault.createBinary(filePath, arrayBuffer);

                          // 更新输入框和背景设置
                          const inputEl = document.getElementById('page-bg-input');
                          if (inputEl) {
                            inputEl.value = filePath;
                          }
                          setBackground('image', filePath);
                        } catch (error) {
                          console.error('上传失败:', error);
                          console.error('上传失败:', error.message);
                        }
                      };
                      input.click();
                    }}
                    style={{
                      padding: '8px 16px',
                      background: '#667eea',
                      border: 'none',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '12px',
                      cursor: 'pointer',
                      whiteSpace: 'nowrap'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.background = '#5568d3'}
                    onMouseLeave={(e) => e.currentTarget.style.background = '#667eea'}
                  >
                    上传
                  </button>
                </div>
                {/* 视频背景设置 */}
                <div style={{ marginTop: '16px', padding: '12px', background: tc('bgPanel'), borderRadius: '8px', border: '1px dashed #ddd' }}>
                  <div 
                    onClick={() => setShowVideoSettings(!showVideoSettings)}
                    style={{ 
                      fontSize: '12px', 
                      color: tc('textSecondary'), 
                      marginBottom: showVideoSettings ? '8px' : '0',
                      fontWeight: '500',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      userSelect: 'none'
                    }}
                  >
                    <span>🎬 动态壁纸（视频）</span>
                    <span style={{ 
                      fontSize: '10px', 
                      transition: 'transform 0.2s',
                      transform: showVideoSettings ? 'rotate(180deg)' : 'rotate(0deg)'
                    }}>▼</span>
                  </div>
                  {showVideoSettings && (
                  <>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <div style={{ flex: 1, position: 'relative' }}>
                      {(() => {
                        // 验证视频 URL 是否有效
                        const validateVideoUrl = (url, onSuccess) => {
                          setVideoUrlError('');

                          // 创建视频对象进行检测
                          const video = document.createElement('video');

                          // 成功加载
                          video.onloadedmetadata = () => {
                            setVideoUrlError('');
                            onSuccess();
                          };

                          // 加载失败
                          video.onerror = () => {
                            setVideoUrlError('视频地址不正确或不支持');
                          };

                          // 开始加载
                          video.src = url;
                        };

                        // 提取视频搜索逻辑为函数
                        const searchVideos = (searchTerm) => {
                          const dropdown = document.getElementById('page-bg-video-dropdown');
                          const list = document.getElementById('page-bg-video-list');

                          if (!dropdown || !list) return;

                          if (searchTerm.length === 0) {
                            dropdown.style.display = 'none';
                            return;
                          }

                          list.innerHTML = '';

                          // 检查是否是 http/https URL
                          if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                            const item = document.createElement('div');
                            item.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; color: #667eea; font-weight: 500;";
                            item.textContent = searchTerm;
                            item.onmousedown = (e) => {
                              e.preventDefault();
                              setVideoUrlError('');
                              validateVideoUrl(searchTerm, () => {
                                setBackground('video', searchTerm);
                              });
                              dropdown.style.display = 'none';
                            };
                            list.appendChild(item);
                            dropdown.style.display = 'block';
                            return;
                          }

                          // 本地文件搜索模式
                          const allFiles = vault.getFiles();
                          const videoExtensions = ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v'];
                          const videoFiles = allFiles.filter(f =>
                            videoExtensions.some(ext => f.path.toLowerCase().endsWith(ext))
                          );

                          // 模糊匹配
                          const matches = videoFiles.filter(f =>
                            f.path.toLowerCase().includes(searchTerm)
                          ).slice(0, 10);

                          if (matches.length === 0) {
                            const noResult = document.createElement('div');
                            noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                            noResult.textContent = '未找到匹配的视频';
                            list.appendChild(noResult);
                          } else {
                            matches.forEach(match => {
                              const item = document.createElement('div');
                              item.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #f0f0f0;";
                              item.textContent = match.path;
                              item.onmousedown = (e) => {
                                e.preventDefault();
                                const inputEl = document.getElementById('page-bg-video-input');
                                if (inputEl) {
                                  inputEl.value = match.path;
                                }
                                setVideoUrlError('');
                                setBackground('video', match.path);
                                dropdown.style.display = 'none';
                              };
                              list.appendChild(item);
                            });

                            dropdown.style.display = 'block';
                          }
                        };

                        return (
                          <>
                          <input
                            id="page-bg-video-input"
                            type="text"
                            placeholder="输入视频路径或 URL"
                            defaultValue={(tempConfig || config).background?.type === 'video' ? (tempConfig || config).background?.value : ''}
                            onClick={(e) => e.stopPropagation()}
                            onFocus={() => {
                              const dropdown = document.getElementById('page-bg-video-dropdown');
                              if (dropdown) dropdown.style.display = 'block';
                              setVideoUrlError('');
                            }}
                            onBlur={(e) => {
                              setTimeout(() => {
                                const dropdown = document.getElementById('page-bg-video-dropdown');
                                if (dropdown) dropdown.style.display = 'none';
                              }, 200);
                              // 失去焦点时自动应用输入的路径
                              const url = e.target.value.trim();
                              if (url) {
                                if (url.startsWith('http://') || url.startsWith('https://')) {
                                  setVideoUrlError('');
                                  validateVideoUrl(url, () => {
                                    setBackground('video', url);
                                  });
                                } else {
                                  setVideoUrlError('');
                                  setBackground('video', url);
                                }
                              }
                            }}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                const url = e.target.value.trim();
                                if (url) {
                                  if (url.startsWith('http://') || url.startsWith('https://')) {
                                    setVideoUrlError('');
                                    validateVideoUrl(url, () => {
                                      setBackground('video', url);
                                    });
                                  } else {
                                    setVideoUrlError('');
                                    setBackground('video', url);
                                  }
                                }
                                e.currentTarget.blur();
                              }
                            }}
                            onCompositionStart={(e) => {
                              e.target.dataset.isComposing = 'true';
                            }}
                            onCompositionEnd={(e) => {
                              e.target.dataset.isComposing = 'false';
                              const url = e.target.value.trim();
                              if (url) {
                                searchVideos(url.toLowerCase());
                              }
                            }}
                            onInput={(e) => {
                              if (e.target.dataset.isComposing === 'true') return;
                              const url = e.target.value.trim();
                              if (url) {
                                searchVideos(url.toLowerCase());
                              }
                            }}
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              fontSize: '12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              outline: 'none',
                              boxSizing: 'border-box'
                            }}
                          />
                          {videoUrlError && (
                            <div style={{
                              color: tc('errorText'),
                              fontSize: '11px',
                              marginTop: '4px'
                            }}>
                              {videoUrlError}
                            </div>
                          )}
                          </>
                        );
                      })()}
                      {/* 搜索结果下拉框 */}
                      <div
                        id="page-bg-video-dropdown"
                        style={{
                          display: 'none',
                          position: 'absolute',
                          top: '100%',
                          left: 0,
                          right: 0,
                          background: tc('bgInput'),
                          border: tc('borderInput'),
                          borderRadius: '6px',
                          boxShadow: tc('shadowPopup'),
                          zIndex: 100,
                          maxHeight: '200px',
                          overflowY: 'auto',
                          marginTop: '4px'
                        }}
                      >
                        <div id="page-bg-video-list"></div>
                      </div>
                    </div>

                    {/* 上传视频按钮 */}
                    <button
                      onClick={() => {
                        const input = document.createElement('input');
                        input.type = 'file';
                        input.accept = 'video/*';
                        input.onchange = async (e) => {
                          const file = e.target.files?.[0];
                          if (!file) return;

                          try {
                            // 生成唯一文件名
                            const timestamp = Date.now();
                            const ext = file.name.split('.').pop() || 'mp4';
                            const fileName = `bg_video_${timestamp}.${ext}`;

                            // 使用 Obsidian API 获取附件保存路径
                            const filePath = await app.fileManager.getAvailablePathForAttachment(fileName, currentFilePath);

                            // 读取文件内容
                            const arrayBuffer = await file.arrayBuffer();

                            // 创建文件
                            await vault.createBinary(filePath, arrayBuffer);

                            // 更新输入框和背景设置
                            const inputEl = document.getElementById('page-bg-video-input');
                            if (inputEl) {
                              inputEl.value = filePath;
                            }
                            setBackground('video', filePath);
                          } catch (error) {
                            console.error('上传失败:', error);
                            console.error('上传失败:', error.message);
                          }
                        };
                        input.click();
                      }}
                      style={{
                        padding: '8px 16px',
                        background: '#667eea',
                        border: 'none',
                        borderRadius: '8px',
                        color: '#fff',
                        fontSize: '12px',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = '#5568d3'}
                      onMouseLeave={(e) => e.currentTarget.style.background = '#667eea'}
                    >
                      上传视频
                    </button>
                  </div>
                  <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                    支持外部 URL、Obsidian 路径或上传视频（支持 .mp4, .webm, .mov 等格式）
                  </div>

                  {/* 视频效果选项 */}
                  <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '8px' }}>
                    <div style={{ fontSize: '11px', color: tc('textSecondary'), marginBottom: '10px', fontWeight: '500' }}>视频效果设置</div>
                    
                    {/* 毛玻璃强度 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary'), fontWeight: 'bold' }}>毛玻璃</span>
                      <input type="range" min="0" max="50" step="1" value={(tempConfig || config).background?.videoFrostedBlur || 0}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoFrostedBlur: parseInt(e.target.value) })}
                        style={{ flex: 1, cursor: 'pointer' }} />
                      <span style={{ fontSize: '11px', width: '35px', textAlign: 'right' }}>{(tempConfig || config).background?.videoFrostedBlur || 0}px</span>
                    </div>


                    {/* 白底不透明 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary'), fontWeight: 'bold' }}>白底不透明</span>
                      <input type="range" min="0" max="100" step="5" value={(tempConfig || config).background?.videoFrostedOpacity || 0}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoFrostedOpacity: parseInt(e.target.value) })}
                        style={{ flex: 1, cursor: 'pointer' }} />
                      <span style={{ fontSize: '11px', width: '35px', textAlign: 'right' }}>{(tempConfig || config).background?.videoFrostedOpacity || 0}%</span>
                    </div>

                    {/* 亮度 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary') }}>亮度</span>
                      <input type="range" min="0" max="200" step="5" value={(tempConfig || config).background?.videoBrightness ?? 100}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoBrightness: parseInt(e.target.value) })}
                        style={{ flex: 1, cursor: 'pointer' }} />
                      <span style={{ fontSize: '11px', width: '35px', textAlign: 'right' }}>{(tempConfig || config).background?.videoBrightness ?? 100}%</span>
                    </div>

                    {/* 对比度 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary') }}>对比度</span>
                      <input type="range" min="0" max="200" step="5" value={(tempConfig || config).background?.videoContrast ?? 100}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoContrast: parseInt(e.target.value) })}
                        style={{ flex: 1, cursor: 'pointer' }} />
                      <span style={{ fontSize: '11px', width: '35px', textAlign: 'right' }}>{(tempConfig || config).background?.videoContrast ?? 100}%</span>
                    </div>

                    {/* 不透明度 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary') }}>不透明度</span>
                      <input type="range" min="0" max="100" step="5" value={(tempConfig || config).background?.videoOpacity ?? 100}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoOpacity: parseInt(e.target.value) })}
                        style={{ flex: 1, cursor: 'pointer' }} />
                      <span style={{ fontSize: '11px', width: '35px', textAlign: 'right' }}>{(tempConfig || config).background?.videoOpacity ?? 100}%</span>
                    </div>

                    {/* 播放速度 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary') }}>播放速度</span>
                      <input type="range" min="0.1" max="3" step="0.1" value={(tempConfig || config).background?.videoSpeed || 1}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoSpeed: parseFloat(e.target.value) })}
                        style={{ flex: 1, cursor: 'pointer' }} />
                      <span style={{ fontSize: '11px', width: '35px', textAlign: 'right' }}>{(tempConfig || config).background?.videoSpeed || 1}x</span>
                    </div>

                    {/* 自动适配 */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '11px', width: '60px', color: tc('textSecondary') }}>自动适配</span>
                      <select value={(tempConfig || config).background?.videoFit || 'cover'}
                        onChange={(e) => setBackground('video', (tempConfig || config).background?.video || '', { videoFit: e.target.value })}
                        style={{ flex: 1, padding: '4px', fontSize: '11px', borderRadius: '4px', border: tc('borderInput'), cursor: 'pointer' }}>
                        <option value="cover">智能裁剪 (Cover) - 推荐，无黑边</option>
                        <option value="contain">完整显示 (Contain) - 可能会有黑边</option>
                        <option value="fill">拉伸铺满 (Fill) - 画面会变形</option>
                      </select>
                    </div>
                  </div>
                  </>
                  )}
                </div>
              </div>
            )}
          </div>


          {/* 添加组件 */}
          <div style={{ marginBottom: '16px', position: 'relative' }}>
            <div style={{ fontSize: '13px', color: tc('textSecondary'), marginBottom: '8px' }}>添加组件</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(90px, 1fr))', gap: '8px' }}>
              {COMPONENT_TYPES.map(type => {
                // 主面板组件已存在时禁用
                const disabled = type.id === 'personal' && (tempConfig || config).components.some(c => c.type === 'personal');
                return (
                <button
                  key={type.id}
                  onClick={() => !disabled && addComponent(type.id)}
                  disabled={disabled}
                  style={{
                    padding: '16px 8px',
                    background: disabled ? tc('cardBgSubtle') : tc('cardBgLight'),
                    border: tc('borderSubtle'),
                    borderRadius: '8px',
                    fontSize: '12px',
                    cursor: disabled ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '6px',
                    transition: 'all 0.2s',
                    minHeight: '60px',
                    justifyContent: 'center',
                    opacity: disabled ? 0.4 : 1
                  }}
                  onMouseEnter={(e) => !disabled && (e.currentTarget.style.background = tc('cardBgMedium'))}
                  onMouseLeave={(e) => !disabled && (e.currentTarget.style.background = tc('cardBgLight'))}
                >
                  <span style={{ fontSize: '24px', lineHeight: 1 }}>{type.icon}</span>
                  <span style={{ lineHeight: 1 }}>{disabled ? type.name + '（已添加）' : type.name}</span>
                </button>
              );
              })}
            </div>
          </div>

          {/* 辅助网格设置菜单 */}
          {showAuxGridSettings && (
            <div
              style={{
                position: 'absolute',
                right: auxGridSettingsPos.right + 'px',
                top: auxGridSettingsPos.top + 'px',
                width: '240px',
                background: 'rgba(255, 255, 255, 0.98)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(0, 0, 0, 0.1)',
                borderRadius: '12px',
                padding: '16px',
                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
                zIndex: 10000
              }}
              onMouseDown={(e) => {
                e.stopPropagation();
                const startX = e.clientX - auxGridSettingsPos.right;
                const startY = e.clientY - auxGridSettingsPos.top;
                const onMove = (moveEvent) => {
                  const newRight = moveEvent.clientX - startX;
                  const newTop = moveEvent.clientY - startY;
                  setAuxGridSettingsPos({ right: Math.max(16, newRight), top: Math.max(16, newTop) });
                };
                const onUp = () => {
                  document.removeEventListener('mousemove', onMove);
                  document.removeEventListener('mouseup', onUp);
                };
                document.addEventListener('mousemove', onMove);
                document.addEventListener('mouseup', onUp);
              }}
            >
              <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '12px', color: tc('textPrimary') }}>辅助网格设置</div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>网格线颜色</label>
                <input
                  type="color"
                  value={auxGrid.lineColor}
                  onChange={(e) => setAuxGrid(prev => ({ ...prev, lineColor: e.target.value }))}
                  onClick={(e) => e.stopPropagation()}
                  style={{
                    width: '100%',
                    height: '36px',
                    border: tc('borderInput'),
                    borderRadius: '6px',
                    cursor: 'pointer',
                    padding: '2px'
                  }}
                />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>网格密度（像素）: {auxGrid.density}px</label>
                <input
                  type="range"
                  min="20"
                  max="200"
                  step="10"
                  value={auxGrid.density}
                  onChange={(e) => setAuxGrid(prev => ({ ...prev, density: parseInt(e.target.value) }))}
                  onClick={(e) => e.stopPropagation()}
                  style={{
                    width: '100%',
                    cursor: 'pointer'
                  }}
                />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>线条样式</label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', cursor: 'pointer' }}>
                    <input
                      type="radio"
                      name="auxGridLineStyle"
                      checked={auxGrid.lineStyle === 'solid'}
                      onChange={() => setAuxGrid(prev => ({ ...prev, lineStyle: 'solid' }))}
                      onClick={(e) => e.stopPropagation()}
                      style={{ cursor: 'pointer' }}
                    />
                    实线
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', cursor: 'pointer' }}>
                    <input
                      type="radio"
                      name="auxGridLineStyle"
                      checked={auxGrid.lineStyle === 'dashed'}
                      onChange={() => setAuxGrid(prev => ({ ...prev, lineStyle: 'dashed' }))}
                      onClick={(e) => e.stopPropagation()}
                      style={{ cursor: 'pointer' }}
                    />
                    虚线
                  </label>
                </div>
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>线条宽度: {auxGrid.lineWidth}px</label>
                <input
                  type="range"
                  min="1"
                  max="3"
                  step="0.5"
                  value={auxGrid.lineWidth}
                  onChange={(e) => setAuxGrid(prev => ({ ...prev, lineWidth: parseFloat(e.target.value) }))}
                  onClick={(e) => e.stopPropagation()}
                  style={{
                    width: '100%',
                    cursor: 'pointer'
                  }}
                />
              </div>
            </div>
          )}

          {/* 已有组件列表 */}
          {currentConfig.components.length > 0 && (
            <div style={{ paddingTop: '16px', borderTop: tc('borderSubtle') }}>
              <div style={{ fontSize: '13px', color: tc('textSecondary'), marginBottom: '8px' }}>组件列表（上方的组件显示在上层）</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: '200px', overflow: 'auto' }}>
                {currentConfig.components.map((comp, index) => {
                  const typeInfo = COMPONENT_TYPES.find(t => t.id === comp.type);
                  const isFirst = index === 0;
                  const isLast = index === currentConfig.components.length - 1;
                  return (
                    <div
                      key={comp.id}
                      style={{
                        padding: '8px 12px',
                        background: tc('cardBgLight'),
                        borderRadius: '6px',
                        fontSize: '12px',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}
                    >
                      <span>{typeInfo?.icon} {(comp.title || typeInfo?.name).replace(/<[^>]*>/g, '')}</span>
                      <div style={{ display: 'flex', gap: '4px' }}>
                        <button
                          onClick={() => reorderComponent(comp.id, 'up')}
                          disabled={isFirst}
                          style={{
                            padding: '4px 8px',
                            background: isFirst ? tc('cardBgLight') : tc('accentBg'),
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '11px',
                            cursor: isFirst ? 'not-allowed' : 'pointer',
                            opacity: isFirst ? 0.5 : 1
                          }}
                          title="向上移动（显示在更上层）"
                        >
                          ↑
                        </button>
                        <button
                          onClick={() => reorderComponent(comp.id, 'down')}
                          disabled={isLast}
                          style={{
                            padding: '4px 8px',
                            background: isLast ? tc('cardBgLight') : tc('accentBg'),
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '11px',
                            cursor: isLast ? 'not-allowed' : 'pointer',
                            opacity: isLast ? 0.5 : 1
                          }}
                          title="向下移动（显示在更下层）"
                        >
                          ↓
                        </button>
                        <button
                          onClick={() => setEditingComponent(comp.id)}
                          style={{
                            padding: '4px 8px',
                            background: tc('accentBg'),
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '11px',
                            cursor: 'pointer'
                          }}
                        >
                          编辑
                        </button>
                        <button
                          onClick={() => deleteComponent(comp.id)}
                          style={{
                            padding: '4px 8px',
                            background: 'rgba(245, 87, 108, 0.2)',
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '11px',
                            cursor: 'pointer'
                          }}
                        >
                          删除
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* 组件编辑弹窗 */}
      {editingComponent && (
        <div
          onClick={(e) => {
            // 如果有文本被选中，不关闭弹窗（避免拖动选择文字时误关闭）
            const selection = window.getSelection();
            if (selection && selection.toString().trim().length > 0) {
              e.stopPropagation();
              return;
            }
            flushPendingUpdates();
            setEditingComponent(null);
          }}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            background: 'rgba(0,0,0,0.5)',
            zIndex: 10001
          }}>
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              position: 'fixed',
              left: '50%',
              top: '50%',
              transform: `translate(calc(-50% + ${editDialogPos.x}px), calc(-50% + ${editDialogPos.y}px))`,
              width: '450px',
              maxHeight: '80vh',
              background: tc('bgInput'),
              borderRadius: '16px',
              padding: '24px',
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
              overflowY: 'auto'
            }}>
            <div 
              style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                marginBottom: '20px',
                cursor: 'move',
                userSelect: 'none'
              }}
              onMouseDown={(e) => {
                if (e.target.tagName === 'BUTTON') return;
                setIsDraggingEditDialog(true);
                setEditDialogDragStart({ x: e.clientX - editDialogPos.x, y: e.clientY - editDialogPos.y });
              }}
            >
              <h3 style={{ margin: 0, fontSize: '18px' }}>编辑组件</h3>
              <button
                onClick={() => { flushPendingUpdates(); setEditingComponent(null); }}
                style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  background: 'transparent',
                  border: 'none',
                  color: tc('textLabel'),
                  fontSize: '20px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: 0
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(0,0,0,0.05)';
                  e.currentTarget.style.color = '#333';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = tc('textLabel');
                }}
              >
                ×
              </button>
            </div>
            {(() => {
              const baseComp = currentConfig.components.find(c => c.id === editingComponent);
              if (!baseComp) return null;
              // 合并 pending 的更新，使编辑弹窗能实时反映用户输入
              const pendingUpdates = pendingUpdatesRef.current[editingComponent];
              const comp = pendingUpdates ? { ...baseComp, ...pendingUpdates } : baseComp;

              const typeInfo = COMPONENT_TYPES.find(t => t.id === comp.type);
              return (
                <div>
                  <div style={{ marginBottom: '16px' }}>
                    <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>
                      组件类型: {typeInfo?.icon} {typeInfo?.name}
                    </label>
                  </div>

                  {comp.type === 'clock' && (() => {
                    const clockIs = { width: '100%', padding: '6px 10px', border: tc('borderInput'), borderRadius: '6px', fontSize: '13px' };
                    const clockSs = { ...clockIs, height: '30px', padding: '4px 8px' };
                    const clockLs = { display: 'block', fontSize: '11px', color: '#888', marginBottom: '2px' };
                    const clockFonts = [
                      { v: '', l: '默认字体' },
                      { v: 'Segoe UI Light', l: 'Segoe UI Light' },
                      { v: "Georgia, 'Times New Roman', serif", l: 'Georgia 衬线' },
                      { v: "'Trebuchet MS', 'Lucida Sans', sans-serif", l: 'Trebuchet MS' },
                      { v: 'Verdana, Geneva, sans-serif', l: 'Verdana' },
                      { v: 'Impact, Charcoal, sans-serif', l: 'Impact 粗体' },
                      { v: "'Palatino Linotype', 'Book Antiqua', Palatino, serif", l: 'Palatino 古典' },
                      { v: "'Courier New', Courier, monospace", l: 'Courier 等宽' },
                      { v: "'Lucida Console', Monaco, monospace", l: 'Lucida Console' },
                      { v: "'Comic Sans MS', cursive", l: 'Comic Sans 手写' },
                      { v: '"Ruthligos", cursive', l: 'Ruthligos 花体' },
                      { v: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", l: '系统默认' },
                      { v: "'Microsoft YaHei', 'PingFang SC', sans-serif", l: '微软雅黑' },
                      { v: "'KaiTi', '楷体', serif", l: '楷体' },
                      { v: "'SimSun', '宋体', serif", l: '宋体' },
                      { v: "'Consolas', 'Monaco', monospace", l: 'Consolas 等宽' },
                      { v: '"Dancing Script", cursive', l: 'Dancing Script 优雅手写' },
                      { v: '"Great Vibes", cursive', l: 'Great Vibes 经典花体' },
                      { v: '"Pacifico", cursive', l: 'Pacifico 潇洒手写' },
                      { v: '"Sacramento", cursive', l: 'Sacramento 轻盈草书' },
                      { v: '"Caveat", cursive', l: 'Caveat 自然手写' },
                      { v: '"Satisfy", cursive', l: 'Satisfy 流畅花体' },
                    ];
                    const clockRg = (title, sf, cf, ff, ds, dcVal, showField, extraContent) => (
                      <div style={{ marginBottom: '10px', padding: '6px 8px', background: tc('bgPanel'), borderRadius: '6px' }}>
                        <div style={{ fontSize: '12px', fontWeight: 600, color: tc('textSecondary'), marginBottom: '5px' }}>{title}</div>
                        <div style={{ display: 'flex', gap: '6px', marginBottom: extraContent ? '4px' : '0', alignItems: 'flex-end' }}>
                          <div style={{ flex: '0 0 56px' }}>
                            <label style={clockLs}>字号</label>
                            <input type="number" defaultValue={comp[sf] || ds}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { [sf]: parseInt(e.target.value) || ds })}
                              onClick={(e) => e.stopPropagation()} onFocus={(e) => e.stopPropagation()} style={clockIs} />
                          </div>
                          <div style={{ flex: '0 0 56px' }}>
                            <label style={clockLs}>颜色</label>
                            <input type="color" defaultValue={comp[cf] || dcVal}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { [cf]: e.target.value })}
                              style={{ width: '100%', height: '30px', border: tc('borderInput'), borderRadius: '6px', cursor: 'pointer', padding: '2px' }} />
                          </div>
                          <div style={{ flex: 1, minWidth: 0 }}>
                            <label style={clockLs}>字体</label>
                            <select defaultValue={comp[ff] || ''}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { [ff]: e.target.value })}
                              onClick={(e) => e.stopPropagation()} style={clockSs}>
                              {clockFonts.map(o => <option key={o.v} value={o.v}>{o.l}</option>)}
                            </select>
                          </div>
                          <div style={{ flex: '0 0 auto', paddingBottom: '2px' }}>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '3px', fontSize: '10px', color: '#888', cursor: 'pointer', whiteSpace: 'nowrap' }}>
                              <input type="checkbox"
                                defaultChecked={comp[showField] !== false}
                                onChange={(e) => debouncedUpdateComponent(comp.id, { [showField]: e.target.checked })}
                                style={{ cursor: 'pointer' }} />
                              显示
                            </label>
                          </div>
                        </div>
                        {extraContent}
                      </div>
                    );
                    return (
                    <>
                      {clockRg('⏱ 时间', 'timeSize', 'timeColor', 'timeFontFamily', 72, '#ffffff', 'showTime', (
                        <div style={{ marginTop: '4px', borderTop: tc('borderSubtle'), paddingTop: '4px' }}>
                          <label style={clockLs}>时间格式</label>
                          <select defaultValue={comp?.timeFormat || 'withSeconds'}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { timeFormat: e.target.value })}
                            onClick={(e) => e.stopPropagation()} style={clockSs}>
                            <option value="withSeconds">显示秒 (时:分:秒)</option>
                            <option value="noSeconds">隐藏秒 (时:分)</option>
                          </select>
                        </div>
                      ))}
                      {clockRg('📅 日期', 'dateFontSize', 'dateColor', 'dateFontFamily', 30, '#5eaf1c', 'showDate')}
                      {clockRg('📆 星期（背景）', 'weekdayFontSize', 'weekdayColor', 'weekdayFontFamily', 140, '#f33652', 'showWeekday')}
                      <div style={{ marginBottom: '10px', padding: '6px 8px', background: tc('bgPanel'), borderRadius: '6px' }}>
                        <div style={{ fontSize: '12px', fontWeight: 600, color: tc('textSecondary'), marginBottom: '5px' }}>📆 星期透明度</div>
                        <label style={clockLs}>透明度: {Math.round((comp?.weekdayOpacity ?? 0.4) * 100)}%</label>
                        <input type="range" min="0" max="100" step="1"
                          defaultValue={Math.round((comp?.weekdayOpacity ?? 0.4) * 100)}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { weekdayOpacity: parseInt(e.target.value) / 100 })}
                          style={{ width: '100%', cursor: 'pointer' }} />
                      </div>
                      {clockRg('💬 格言', 'mottoFontSize', 'mottoColor', 'mottoFontFamily', 14, '#ffffff', 'showMotto')}
                      {clockRg('👋 问候语', 'greetingFontSize', 'greetingColor', 'greetingFontFamily', 20, '#ffffff', 'showGreeting')}
                      <div style={{ marginBottom: '10px' }}>
                        <label style={clockLs}>格言内容（每行一句，随机显示）</label>
                        <textarea
                          defaultValue={comp.mottoes || "所有的伟大，都源于一个勇敢的开始。\n心有山海，静而无边。\n万物皆有裂痕，那是光照进来的地方。\n专注当下，便是胜境。\n凡是过往，皆为序章。"}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { mottoes: e.target.value })}
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          onMouseDown={(e) => e.stopPropagation()}
                          style={{ ...clockIs, minHeight: '80px', resize: 'vertical' }}
                        />
                      </div>
                    </>
                    );
                  })()}

                  {comp.type === 'text' && (
                    <>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题（支持HTML）</label>
                        <input
                          type="text"
                          defaultValue={comp.title}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showTitle !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { showTitle: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示标题
                        </label>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`bgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                              style={{ cursor: 'pointer' }}
                            />
                            毛玻璃
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`bgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                              style={{ cursor: 'pointer' }}
                            />
                            柔边阴影
                          </label>
                        </div>

                        {/* 柔边阴影设置 */}
                        {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                              {/* 自定义调色板 */}
                              <div style={{ flex: '0 0 60px' }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                <input
                                  type="color"
                                  defaultValue={comp?.bgColor || '#ffffff'}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgColor: e.target.value })}
                                  style={{
                                    width: '100%',
                                    height: '36px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    padding: '2px'
                                  }}
                                />
                              </div>

                              {/* 透明度滑块 */}
                              <div style={{ flex: 1 }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                  背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                </label>
                                <input
                                  type="range"
                                  min="0"
                                  max="100"
                                  step="5"
                                  defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                  style={{
                                    width: '100%',
                                    cursor: 'pointer'
                                  }}
                                />
                              </div>
                              <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                  <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => debouncedUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                  显示边框
                                </label>
                              </div>
                            </div>
                            <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                              <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                            </div>
                          </div>
                        )}
                        {(comp?.backgroundStyle || 'glass') === 'glass' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                            <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                          </div>
                        )}
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>内边距（像素）</label>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px' }}>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>上</label>
                            <input
                              type="number"
                              defaultValue={comp.paddingTop ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingTop: parseInt(e.target.value) || 0 })}
                              style={{
                                width: '100%',
                                padding: '6px 8px',
                                border: tc('borderInput'),
                                borderRadius: '4px',
                                fontSize: '13px'
                              }}
                            />
                          </div>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>下</label>
                            <input
                              type="number"
                              defaultValue={comp.paddingBottom ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingBottom: parseInt(e.target.value) || 0 })}
                              style={{
                                width: '100%',
                                padding: '6px 8px',
                                border: tc('borderInput'),
                                borderRadius: '4px',
                                fontSize: '13px'
                              }}
                            />
                          </div>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>左</label>
                            <input
                              type="number"
                              defaultValue={comp.paddingLeft ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingLeft: parseInt(e.target.value) || 0 })}
                              style={{
                                width: '100%',
                                padding: '6px 8px',
                                border: tc('borderInput'),
                                borderRadius: '4px',
                                fontSize: '13px'
                              }}
                            />
                          </div>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>右</label>
                            <input
                              type="number"
                              defaultValue={comp.paddingRight ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingRight: parseInt(e.target.value) || 0 })}
                              style={{
                                width: '100%',
                                padding: '6px 8px',
                                border: tc('borderInput'),
                                borderRadius: '4px',
                                fontSize: '13px'
                              }}
                            />
                          </div>
                        </div>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>内容</label>
                        <textarea
                          defaultValue={comp.content}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { content: e.target.value })}
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          onMouseDown={(e) => e.stopPropagation()}
                          style={{
                            width: '100%',
                            minHeight: '80px',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px',
                            resize: 'vertical'
                          }}
                        />
                      </div>
                    </>
                  )}

                  {comp.type === 'link' && (
                    <>
                      {/* 显示标题选项 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showTitle !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { showTitle: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示标题（标题将显示在图标下方）
                        </label>
                      </div>

                      {/* 标题输入 */}
                      {comp.showTitle !== false && (
                        <div style={{ marginBottom: '12px' }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题</label>
                          <input
                            type="text"
                            defaultValue={comp.title || ''}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                            placeholder="输入标题"
                            onClick={(e) => e.stopPropagation()}
                            onFocus={(e) => e.stopPropagation()}
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px'
                            }}
                          />
                        </div>
                      )}

                      {/* 链接模式选择 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>链接模式</label>
                        <div style={{ display: 'flex', gap: '16px' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`linkMode-${comp.id}`}
                              defaultChecked={(comp?.linkMode || 'link') === 'link'}
                              onChange={() => {
                                debouncedUpdateComponent(comp.id, { linkMode: 'link' });
                                // 切换到链接模式时，重置命令选择器状态
                                setCommandSelectorState({
                                  searchQuery: '',
                                  showList: false,
                                  isComposing: false,
                                  currentComponentId: comp.id,
                                  isUserEditing: false
                                });
                              }}
                              style={{ cursor: 'pointer' }}
                            />
                            链接
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`linkMode-${comp.id}`}
                              defaultChecked={(comp?.linkMode || 'link') === 'command'}
                              onChange={() => {
                                debouncedUpdateComponent(comp.id, { linkMode: 'command' });
                                // 切换到命令模式时，重置链接输入状态
                                setLinkInputState({
                                  value: '',
                                  currentComponentId: comp.id
                                });
                              }}
                              style={{ cursor: 'pointer' }}
                            />
                            命令
                          </label>
                        </div>
                      </div>

                      {/* 链接输入 */}
                      {(comp?.linkMode || 'link') === 'link' ? (
                        (() => {
                          const linkInputId = `link-comp-input-${comp.id}`;
                          const dropdownId = `link-comp-dropdown-${comp.id}`;
                          const listId = `link-comp-list-${comp.id}`;

                          // 文件搜索逻辑
                          const searchFiles = (searchTerm) => {
                            const dropdown = document.getElementById(dropdownId);
                            const list = document.getElementById(listId);

                            if (!dropdown || !list) return;

                            // 如果是 URL，不显示搜索结果
                            if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                              dropdown.style.display = 'none';
                              return;
                            }

                            if (searchTerm.length === 0) {
                              dropdown.style.display = 'none';
                              return;
                            }

                            // 获取所有文件
                            const allFiles = app.vault.getFiles();

                            // 模糊匹配文件路径（支持所有文件类型）
                            const matches = allFiles.filter(f =>
                              f.path.toLowerCase().includes(searchTerm)
                            ).slice(0, 10);

                            list.innerHTML = '';

                            if (matches.length === 0) {
                              const noResult = document.createElement('div');
                              noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                              noResult.textContent = '未找到匹配的文件';
                              list.appendChild(noResult);
                            } else {
                              matches.forEach(match => {
                                const itemEl = document.createElement('div');
                                itemEl.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #f0f0f0;";
                                itemEl.textContent = match.path;
                                itemEl.onmousedown = (e) => {
                                  e.preventDefault();
                                  const inputEl = document.getElementById(linkInputId);
                                  if (inputEl) {
                                    inputEl.value = match.path;
                                  }
                                  const newValue = match.path;
                                  setLinkInputState({
                                    value: newValue,
                                    currentComponentId: comp.id
                                  });
                                  debouncedUpdateComponent(comp.id, { link: newValue });
                                  dropdown.style.display = 'none';
                                };
                                list.appendChild(itemEl);
                              });

                              dropdown.style.display = 'block';
                            }
                          };

                          return (
                            <div style={{ marginBottom: '12px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>链接地址</label>
                              <div style={{ position: 'relative' }}>
                                <input
                                  key={`link-input-${comp.id}`}
                                  id={linkInputId}
                                  type="text"
                                  value={linkInputState.currentComponentId === comp.id ? linkInputState.value : (comp?.link || '')}
                                  onClick={(e) => e.stopPropagation()}
                                  onFocus={(e) => {
                                    // 初始化或重置链接输入状态
                                    if (linkInputState.currentComponentId !== comp.id) {
                                      setLinkInputState({
                                        value: comp?.link || '',
                                        currentComponentId: comp.id
                                      });
                                    }
                                    const dropdown = document.getElementById(dropdownId);
                                    if (dropdown) dropdown.style.display = 'block';
                                  }}
                                  onBlur={() => {
                                    setTimeout(() => {
                                      const dropdown = document.getElementById(dropdownId);
                                      if (dropdown) dropdown.style.display = 'none';
                                    }, 200);
                                  }}
                                  onCompositionStart={(e) => {
                                    e.target.dataset.isComposing = 'true';
                                  }}
                                  onCompositionEnd={(e) => {
                                    e.target.dataset.isComposing = 'false';
                                    const newValue = e.target.value;
                                    setLinkInputState(prev => ({ ...prev, value: newValue }));
                                    debouncedUpdateComponent(comp.id, { link: newValue });
                                    searchFiles(newValue.toLowerCase());
                                  }}
                                  onInput={(e) => {
                                    if (e.target.dataset.isComposing === 'true') return;
                                    const newValue = e.target.value;
                                    setLinkInputState(prev => ({ ...prev, value: newValue }));
                                    debouncedUpdateComponent(comp.id, { link: newValue });
                                    searchFiles(newValue.toLowerCase());
                                  }}
                                  placeholder="https://example.com 或 搜索文件..."
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '14px'
                                  }}
                                />
                                {/* 搜索结果下拉框 */}
                                <div
                                  id={dropdownId}
                                  style={{
                                    display: 'none',
                                    position: 'absolute',
                                    top: '100%',
                                    left: 0,
                                    right: 0,
                                    background: tc('bgInput'),
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    boxShadow: tc('shadowPopup'),
                                    zIndex: 100,
                                    maxHeight: '180px',
                                    overflowY: 'auto',
                                    marginTop: '4px'
                                  }}
                                >
                                  <div id={listId}></div>
                                </div>
                              </div>
                              <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                                支持外部 URL（https://...）或 搜索选择文件
                              </div>
                            </div>
                          );
                        })()
                      ) : (
                        (() => {
                          // 命令模式：搜索并选择命令
                          const commandsResult = commands.listCommands();
                          const allCommands = Array.isArray(commandsResult) ? commandsResult : [];
                          const savedCommandId = comp?.commandId || '';
                          const savedCommand = allCommands.find(c => c.id === savedCommandId);

                          // 检测组件变化，重置状态
                          if (commandSelectorState.currentComponentId !== comp.id) {
                            setCommandSelectorState({
                              searchQuery: '',
                              showList: false,
                              isComposing: false,
                              currentComponentId: comp.id,
                              isUserEditing: false
                            });
                          }

                          // 简单的命令过滤（不使用 useMemo）
                          let filteredCommands = allCommands.slice(0, 20);
                          if (commandSelectorState.searchQuery.trim() && !commandSelectorState.isComposing) {
                            const search = commandSelectorState.searchQuery.toLowerCase();
                            filteredCommands = allCommands
                              .filter(cmd => cmd.name.toLowerCase().includes(search))
                              .slice(0, 20);
                          }

                          return (
                            <div style={{ marginBottom: '12px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>选择命令</label>
                              <div style={{ position: 'relative' }}>
                                <input
                                  type="text"
                                  value={commandSelectorState.isUserEditing ? commandSelectorState.searchQuery : (commandSelectorState.searchQuery || savedCommand?.name || '')}
                                  onChange={(e) => {
                                    setCommandSelectorState(prev => ({ ...prev, searchQuery: e.target.value, isUserEditing: true }));
                                    if (!commandSelectorState.isComposing) {
                                      setCommandSelectorState(prev => ({ ...prev, showList: true }));
                                    }
                                  }}
                                  onCompositionStart={() => setCommandSelectorState(prev => ({ ...prev, isComposing: true }))}
                                  onCompositionEnd={(e) => {
                                    setCommandSelectorState(prev => ({ ...prev, isComposing: false, searchQuery: e.target.value, showList: true }));
                                  }}
                                  onFocus={(e) => {
                                    e.stopPropagation();
                                    setCommandSelectorState(prev => ({ 
                                      ...prev, 
                                      showList: true, 
                                      searchQuery: '',
                                      isUserEditing: true 
                                    }));
                                  }}
                                  onBlur={() => {
                                    // 延迟隐藏，以便点击事件能够触发
                                    setTimeout(() => setCommandSelectorState(prev => ({ ...prev, showList: false, isUserEditing: false })), 200);
                                  }}
                                  placeholder="搜索命令..."
                                  onClick={(e) => e.stopPropagation()}
                                  onMouseDown={(e) => e.stopPropagation()}
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '14px'
                                  }}
                                />
                                {commandSelectorState.showList && filteredCommands.length > 0 && (
                                  <div style={{
                                    position: 'absolute',
                                    top: '100%',
                                    left: 0,
                                    right: 0,
                                    maxHeight: '200px',
                                    overflowY: 'auto',
                                    background: tc('bgInput'),
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    marginTop: '4px',
                                    boxShadow: tc('shadowPopup'),
                                    zIndex: 10
                                  }}>
                                    {filteredCommands.map(cmd => (
                                      <div
                                        key={cmd.id}
                                        onClick={(e) => {
                                          e.stopPropagation();
                                          setCommandSelectorState(prev => ({ ...prev, searchQuery: cmd.name, showList: false, isUserEditing: false }));
                                          debouncedUpdateComponent(comp.id, { commandId: cmd.id });
                                        }}
                                        onMouseDown={(e) => e.preventDefault()}
                                        style={{
                                          padding: '10px 12px',
                                          cursor: 'pointer',
                                          borderBottom: `1px solid #f0f0f0`,
                                          fontSize: '13px',
                                          background: cmd.id === savedCommandId ? tc('accentSubtle') : '#fff'
                                        }}
                                        onMouseEnter={(e) => {
                                          e.currentTarget.style.background = tc('bgHover');
                                        }}
                                        onMouseLeave={(e) => {
                                          e.currentTarget.style.background = cmd.id === savedCommandId ? tc('accentSubtle') : '#fff';
                                        }}
                                      >
                                        {cmd.name}
                                      </div>
                                    ))}
                                  </div>
                                )}
                                {savedCommand && !commandSelectorState.isUserEditing && (
                                  <div style={{ fontSize: '11px', color: tc('successText'), marginTop: '4px' }}>
                                    ✓ 已选择: {savedCommand.name}
                                  </div>
                                )}
                              </div>
                            </div>
                          );
                        })()
                      )}

                      {/* 图标选择 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>选择图标</label>
                        <div style={{
                          display: 'grid',
                          gridTemplateColumns: 'repeat(5, 1fr)',
                          gap: '8px',
                          marginBottom: '12px'
                        }}>
                          {[
                            { name: 'home', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>' },
                            { name: 'diary', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>' },
                            { name: 'search', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>' },
                            { name: 'settings', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>' },
                            { name: 'star', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>' },
                            { name: 'calendar', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>' },
                            { name: 'check', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>' },
                            { name: 'tag', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>' },
                            { name: 'folder', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>' },
                            { name: 'link', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>' },
                            { name: 'globe', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>' },
                            { name: 'image', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>' },
                            { name: 'music', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>' },
                            { name: 'video', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>' },
                            { name: 'archive', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect><line x1="10" y1="12" x2="14" y2="12"></line></svg>' },
                          ].map(icon => (
                            <div
                              key={icon.name}
                              onClick={() => debouncedUpdateComponent(comp.id, { iconSvg: icon.svg })}
                              style={{
                                width: '56px',
                                height: '56px',
                                padding: '8px',
                                border: (comp?.iconSvg || '') === icon.svg ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                                borderRadius: '6px',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                background: (comp?.iconSvg || '') === icon.svg ? tc('accentSubtle') : tc('bgInput'),
                                transition: 'all 0.2s'
                              }}
                              onMouseEnter={(e) => {
                                if ((comp?.iconSvg || '') !== icon.svg) {
                                  e.currentTarget.style.background = tc('bgHover');
                                }
                              }}
                              onMouseLeave={(e) => {
                                if ((comp?.iconSvg || '') !== icon.svg) {
                                  e.currentTarget.style.background = tc('bgInput');
                                }
                              }}
                              title={icon.name}
                            >
                              <div dangerouslySetInnerHTML={{ __html: sanitizeSvg(icon.svg) }} style={{ width: '32px', height: '32px', color: tc('accent'), display: 'flex', alignItems: 'center', justifyContent: 'center' }} />
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* 自定义图标导入 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>导入自定义图标（SVG）</label>
                        <textarea
                          defaultValue={comp?.iconSvg || ''}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { iconSvg: e.target.value })}
                          placeholder="粘贴 SVG 代码..."
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          onMouseDown={(e) => e.stopPropagation()}
                          style={{
                            width: '100%',
                            minHeight: '80px',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontFamily: 'monospace',
                            resize: 'vertical'
                          }}
                        />
                      </div>

                      {/* 使用说明 */}
                      <div style={{
                        padding: '12px',
                        background: tc('accentSubtle'),
                        borderRadius: '8px',
                        fontSize: '11px',
                        color: tc('accent'),
                        lineHeight: '1.6'
                      }}>
                        <div style={{ fontWeight: '600', marginBottom: '6px' }}>💡 图标获取方法：</div>
                        <div>访问 <a href="https://icon-icons.com/" target="_blank" style={{ color: tc('accent') }}>https://icon-icons.com/</a> 搜索图标</div>
                        <div>点击图标后，点击「copiar SVG」按钮复制 SVG 代码</div>
                        <div>然后粘贴到上方的「导入自定义图标」文本框中</div>
                      </div>
                    </>
                  )}

                  {comp.type === 'query' && (
                    <>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题</label>
                        <input
                          type="text"
                          defaultValue={comp.title}
                          onClick={(e) => e.stopPropagation()}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                        <div style={{ flex: 1 }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>查询方式</label>
                          <select
                            defaultValue={comp.queryType || 'recent'}
                            onClick={(e) => e.stopPropagation()}
                            onChange={(e) => {
                              debouncedUpdateComponent(comp.id, { queryType: e.target.value });
                            }}
                            style={{
                              width: '100%',
                              padding: '10px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px',
                              backgroundColor: tc('bgInput'),
                              height: '42px'
                            }}
                          >
                            <option value="recent">最近笔记</option>
                            <option value="tag">按标签</option>
                            <option value="path">按路径</option>
                            <option value="property">按笔记属性</option>
                            <option value="custom">自定义查询</option>
                          </select>
                        </div>
                        <div style={{ flex: 1 }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>排序方式</label>
                          <select
                            defaultValue={comp.sortBy || 'mtime-desc'}
                            disabled={['recent', 'custom'].includes(comp.queryType || 'recent')}
                            onClick={(e) => e.stopPropagation()}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { sortBy: e.target.value })}
                            style={{
                              width: '100%',
                              padding: '10px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px',
                              backgroundColor: ['recent', 'custom'].includes(comp.queryType || 'recent') ? tc('bgPanel') : tc('bgInput'),
                              height: '42px',
                              cursor: ['recent', 'custom'].includes(comp.queryType || 'recent') ? 'not-allowed' : 'pointer'
                            }}
                          >
                            <option value="name-asc">文件名（A-Z）</option>
                            <option value="name-desc">文件名（Z-A）</option>
                            <option value="ctime-desc">创建时间（新-旧）</option>
                            <option value="ctime-asc">创建时间（旧-新）</option>
                            <option value="mtime-desc">修改时间（新-旧）</option>
                            <option value="mtime-asc">修改时间（旧-新）</option>
                          </select>
                        </div>
                      </div>
                      {comp.queryType === 'tag' && (
                        <div style={{ marginBottom: '12px' }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标签名</label>
                          <input
                            type="text"
                            defaultValue={comp.tagName || ''}
                            placeholder="例如: work、日记、读书"
                            onClick={(e) => e.stopPropagation()}
                            onFocus={(e) => e.stopPropagation()}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { tagName: e.target.value })}
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px'
                            }}
                          />
                          <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>输入标签名，例如：work 或 日记</div>
                        </div>
                      )}
                      {comp.queryType === 'path' && (
                        <div style={{ marginBottom: '12px' }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>路径名</label>
                          <input
                            type="text"
                            defaultValue={comp.pathName || ''}
                            placeholder="例如: 工作/项目、日记/2025"
                            onClick={(e) => e.stopPropagation()}
                            onFocus={(e) => e.stopPropagation()}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { pathName: e.target.value })}
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px'
                            }}
                          />
                          <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>输入文件夹路径，例如：工作/项目</div>
                        </div>
                      )}
                      {comp.queryType === 'property' && (
                        <div style={{ marginBottom: '12px' }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>属性名</label>
                          <input
                            type="text"
                            defaultValue={comp.propName || ''}
                            placeholder="例如: 状态 或 状态=完成"
                            onClick={(e) => e.stopPropagation()}
                            onFocus={(e) => e.stopPropagation()}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { propName: e.target.value })}
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px'
                            }}
                          />
                          <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                            输入属性名查询有该属性的笔记，或输入 属性名=值 精确匹配
                          </div>
                        </div>
                      )}
                      {comp.queryType === 'custom' && (
                        <div style={{ marginBottom: '12px' }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>查询语句</label>
                          <textarea
                            id={"custom-query-" + comp.id}
                            defaultValue={comp.query || '@page'}
                            onClick={(e) => e.stopPropagation()}
                            onFocus={(e) => e.stopPropagation()}
                            onMouseDown={(e) => e.stopPropagation()}
                            placeholder="@page and $path.contains(&quot;日记&quot;)"
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              border: tc('borderInput'),
                              borderRadius: '6px',
                              fontSize: '14px',
                              minHeight: '80px',
                              fontFamily: 'monospace',
                              resize: 'vertical'
                            }}
                          />
                          <div id={"custom-query-error-" + comp.id} style={{ fontSize: '12px', color: '#e53e3e', marginTop: '4px', display: 'none' }}>
                            查询命令不合法
                          </div>
                          <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                            示例: @page and #work、@page and path("日记")、exists(状态)
                          </div>
                          <button
                            id={"custom-query-btn-" + comp.id}
                            onClick={(e) => {
                              e.stopPropagation();
                              const textarea = document.getElementById("custom-query-" + comp.id);
                              const errorDiv = document.getElementById("custom-query-error-" + comp.id);
                              if (textarea) {
                                const query = textarea.value.trim();
                                if (!query) {
                                  if (errorDiv) {
                                    errorDiv.textContent = '请输入查询语句';
                                    errorDiv.style.display = 'block';
                                  }
                                  return;
                                }
                                try {
                                  // 尝试执行查询以验证语法
                                  dc.query(query);
                                  // 验证成功，更新配置
                                  debouncedUpdateComponent(comp.id, { query: query });
                                  if (errorDiv) {
                                    errorDiv.style.display = 'none';
                                  }
                                } catch (error) {
                                  // 验证失败，显示错误
                                  if (errorDiv) {
                                    errorDiv.textContent = '查询命令不合法';
                                    errorDiv.style.display = 'block';
                                  }
                                }
                              }
                            }}
                            style={{
                              marginTop: '8px',
                              padding: '8px 16px',
                              background: '#667eea',
                              color: '#fff',
                              border: 'none',
                              borderRadius: '6px',
                              fontSize: '13px',
                              cursor: 'pointer',
                              width: '100%'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = '#5568d3'}
                            onMouseLeave={(e) => e.currentTarget.style.background = '#667eea'}
                          >
                            应用查询
                          </button>
                        </div>
                      )}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>显示数量</label>
                        <input
                          type="number"
                          defaultValue={comp.maxItems}
                          onClick={(e) => e.stopPropagation()}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { maxItems: parseInt(e.target.value) })}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>

                      {/* 外框样式设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`queryBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                              style={{ cursor: 'pointer' }}
                            />
                            毛玻璃
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`queryBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                              style={{ cursor: 'pointer' }}
                            />
                            柔边阴影
                          </label>
                        </div>

                        {/* 柔边阴影背景设置 */}
                        {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                              {/* 自定义调色板 */}
                              <div style={{ flex: '0 0 60px' }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                <input
                                  type="color"
                                  defaultValue={comp?.bgColor || '#ffffff'}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgColor: e.target.value })}
                                  style={{
                                    width: '100%',
                                    height: '36px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    padding: '2px'
                                  }}
                                />
                              </div>

                              {/* 透明度滑块 */}
                              <div style={{ flex: 1 }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                  背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                </label>
                                <input
                                  type="range"
                                  min="0"
                                  max="100"
                                  step="5"
                                  defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                  style={{
                                    width: '100%',
                                    cursor: 'pointer'
                                  }}
                                />
                              </div>
                              <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                  <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => debouncedUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                  显示边框
                                </label>
                              </div>
                            </div>
                            <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                              <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                            </div>
                          </div>
                        )}
                        {(comp?.backgroundStyle || 'glass') === 'glass' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                            <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                          </div>
                        )}
                      </div>
                    </>
                  )}

                  {comp.type === 'stats' && (
                    <div style={{ marginBottom: '12px' }}>
                      <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题</label>
                      <input
                        type="text"
                        defaultValue={comp.title}
                        onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                        onClick={(e) => e.stopPropagation()}
                        onFocus={(e) => e.stopPropagation()}
                        style={{
                          width: '100%',
                          padding: '8px 12px',
                          border: tc('borderInput'),
                          borderRadius: '6px',
                          fontSize: '14px'
                        }}
                      />
                    </div>
                  )}

                  {comp.type === 'search' && (
                    <>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>占位符文本</label>
                        <input
                          type="text"
                          defaultValue={comp.placeholder || '搜索笔记...'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { placeholder: e.target.value })}
                          placeholder="搜索笔记..."
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>组件宽度</label>
                        <input
                          type="number"
                          defaultValue={comp.width || 350}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { width: parseInt(e.target.value) })}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>组件高度</label>
                        <input
                          type="number"
                          defaultValue={comp.height || 400}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { height: parseInt(e.target.value) })}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>最大结果数</label>
                        <input
                          type="number"
                          defaultValue={comp.maxItems || 10}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { maxItems: parseInt(e.target.value) })}
                          min={1}
                          max={50}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>

                      {/* 外框样式设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`searchBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                              style={{ cursor: 'pointer' }}
                            />
                            毛玻璃
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`searchBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                              style={{ cursor: 'pointer' }}
                            />
                            柔边阴影
                          </label>
                        </div>

                        {/* 柔边阴影背景设置 */}
                        {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                              {/* 自定义调色板 */}
                              <div style={{ flex: '0 0 60px' }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                <input
                                  type="color"
                                  defaultValue={comp?.bgColor || '#ffffff'}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgColor: e.target.value })}
                                  style={{
                                    width: '100%',
                                    height: '36px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    padding: '2px'
                                  }}
                                />
                              </div>

                              {/* 透明度滑块 */}
                              <div style={{ flex: 1 }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                  背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                </label>
                                <input
                                  type="range"
                                  min="0"
                                  max="100"
                                  step="5"
                                  defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                  style={{
                                    width: '100%',
                                    cursor: 'pointer'
                                  }}
                                />
                              </div>
                              <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                  <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => debouncedUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                  显示边框
                                </label>
                              </div>
                            </div>
                            <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                              <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                            </div>
                          </div>
                        )}
                        {(comp?.backgroundStyle || 'glass') === 'glass' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                            <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                          </div>
                        )}
                      </div>
                    </>
                  )}

                  {comp.type === 'note' && (
                    <>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题（支持HTML）</label>
                        <input
                          type="text"
                          defaultValue={comp.title}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showTitle !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { showTitle: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示标题
                        </label>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>便笺样式</label>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '6px' }}>
                          <button
                            onClick={() => debouncedUpdateComponent(comp.id, { noteStyle: 'yellow' })}
                            style={{
                              padding: '10px 8px',
                              background: (comp?.noteStyle || 'yellow') === 'yellow' ? '#fff394' : tc('bgPanel'),
                              border: (comp?.noteStyle || 'yellow') === 'yellow' ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                              borderRadius: '2px',
                              fontSize: '12px',
                              color: '#222',
                              cursor: 'pointer',
                              transition: 'all 0.2s'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = '#fff394'}
                            onMouseLeave={(e) => {
                              if ((comp?.noteStyle || 'yellow') !== 'yellow') {
                                e.currentTarget.style.background = tc('bgPanel');
                              }
                            }}
                          >
                            📒 经典黄
                          </button>
                          <button
                            onClick={() => debouncedUpdateComponent(comp.id, { noteStyle: 'white' })}
                            style={{
                              padding: '10px 8px',
                              background: comp?.noteStyle === 'white' ? '#ffffff' : tc('bgPanel'),
                              border: comp?.noteStyle === 'white' ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                              borderRadius: '2px',
                              fontSize: '12px',
                              color: '#222',
                              cursor: 'pointer',
                              transition: 'all 0.2s'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = '#ffffff'}
                            onMouseLeave={(e) => {
                              if (comp?.noteStyle !== 'white') {
                                e.currentTarget.style.background = tc('bgPanel');
                              }
                            }}
                          >
                            📄 简约白
                          </button>
                          <button
                            onClick={() => debouncedUpdateComponent(comp.id, { noteStyle: 'brown' })}
                            style={{
                              padding: '10px 8px',
                              background: comp?.noteStyle === 'brown' ? '#f9f1e6' : tc('bgPanel'),
                              border: comp?.noteStyle === 'brown' ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                              borderRadius: '2px',
                              fontSize: '12px',
                              color: '#222',
                              cursor: 'pointer',
                              transition: 'all 0.2s'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = '#f9f1e6'}
                            onMouseLeave={(e) => {
                              if (comp?.noteStyle !== 'brown') {
                                e.currentTarget.style.background = tc('bgPanel');
                              }
                            }}
                          >
                            📜 牛皮纸
                          </button>
                          <button
                            onClick={() => debouncedUpdateComponent(comp.id, { noteStyle: 'glass' })}
                            style={{
                              padding: '10px 8px',
                              background: comp?.noteStyle === 'glass' ? 'rgba(255, 255, 255, 0.8)' : tc('bgPanel'),
                              border: comp?.noteStyle === 'glass' ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                              borderRadius: '2px',
                              fontSize: '12px',
                              color: '#1f2937',
                              cursor: 'pointer',
                              transition: 'all 0.2s'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.9)'}
                            onMouseLeave={(e) => {
                              if (comp?.noteStyle !== 'glass') {
                                e.currentTarget.style.background = tc('bgPanel');
                              }
                            }}
                          >
                            🪟 毛玻璃
                          </button>
                        </div>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', cursor: comp?.noteStyle === 'glass' ? 'not-allowed' : 'pointer', color: comp?.noteStyle === 'glass' ? tc('textFaint') : tc('textSecondary') }}>
                            <input
                              type="checkbox"
                              checked={comp?.enableTilt !== false}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { enableTilt: e.target.checked })}
                              disabled={comp?.noteStyle === 'glass'}
                              onClick={(e) => e.stopPropagation()}
                              style={{ cursor: comp?.noteStyle === 'glass' ? 'not-allowed' : 'pointer' }}
                            />
                            倾斜效果
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', cursor: comp?.noteStyle === 'glass' ? 'not-allowed' : 'pointer', color: comp?.noteStyle === 'glass' ? tc('textFaint') : tc('textSecondary') }}>
                            <input
                              type="checkbox"
                              checked={comp?.enableFold !== false}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { enableFold: e.target.checked })}
                              disabled={comp?.noteStyle === 'glass'}
                              onClick={(e) => e.stopPropagation()}
                              style={{ cursor: comp?.noteStyle === 'glass' ? 'not-allowed' : 'pointer' }}
                            />
                            折角效果
                          </label>
                        </div>
                      </div>
                      {comp?.noteStyle === 'white' && (
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>便笺颜色</label>
                        <input
                          type="color"
                          defaultValue={comp?.noteBgColor || '#ffffff'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { noteBgColor: e.target.value })}
                          style={{
                            width: '60px',
                            height: '36px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            cursor: 'pointer',
                            padding: '2px'
                          }}
                        />
                      </div>
                      )}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>内边距（像素）</label>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px' }}>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>上</label>
                            <input type="number" defaultValue={comp?.paddingTop ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingTop: parseInt(e.target.value) || 0 })}
                              style={{ width: '100%', padding: '6px 8px', border: tc('borderInput'), borderRadius: '4px', fontSize: '13px' }} />
                          </div>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>下</label>
                            <input type="number" defaultValue={comp?.paddingBottom ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingBottom: parseInt(e.target.value) || 0 })}
                              style={{ width: '100%', padding: '6px 8px', border: tc('borderInput'), borderRadius: '4px', fontSize: '13px' }} />
                          </div>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>左</label>
                            <input type="number" defaultValue={comp?.paddingLeft ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingLeft: parseInt(e.target.value) || 0 })}
                              style={{ width: '100%', padding: '6px 8px', border: tc('borderInput'), borderRadius: '4px', fontSize: '13px' }} />
                          </div>
                          <div>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textLabel'), marginBottom: '4px' }}>右</label>
                            <input type="number" defaultValue={comp?.paddingRight ?? 24}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { paddingRight: parseInt(e.target.value) || 0 })}
                              style={{ width: '100%', padding: '6px 8px', border: tc('borderInput'), borderRadius: '4px', fontSize: '13px' }} />
                          </div>
                        </div>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>字体</label>
                        <select
                          defaultValue={comp?.fontFamily || 'default'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { fontFamily: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '10px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '13px',
                            minHeight: '38px'
                          }}
                        >
                          <option value="default">微软雅黑</option>
                          <option value="songti">宋体</option>
                          <option value="kaiti">楷体</option>
                          <option value="heiti">黑体</option>
                          <option value="mono">等宽字体</option>
                        </select>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>字体大小（像素）</label>
                        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                          <input
                            type="range"
                            min="10"
                            max="24"
                            step="1"
                            defaultValue={comp?.fontSize || 14}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { fontSize: parseInt(e.target.value) })}
                            style={{ flex: 1 }}
                          />
                          <span style={{ fontSize: '14px', color: tc('textSecondary'), minWidth: '40px', textAlign: 'center' }}>
                            {comp?.fontSize || 14}px
                          </span>
                        </div>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>初始内容（支持HTML）</label>
                        <textarea
                          defaultValue={comp.content}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { content: e.target.value })}
                          onClick={(e) => e.stopPropagation()}
                          onFocus={(e) => e.stopPropagation()}
                          onMouseDown={(e) => e.stopPropagation()}
                          style={{
                            width: '100%',
                            minHeight: '100px',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px',
                            resize: 'vertical'
                          }}
                        />
                      </div>
                      <div style={{ padding: '8px 12px', background: tc('accentSubtle'), borderRadius: '6px', fontSize: '11px', color: tc('accent') }}>
                        💡 便笺可以直接点击编辑，编辑完成后自动保存
                      </div>

                      {/* 外框样式设置（仅在毛玻璃样式时显示） */}
                      {comp?.noteStyle === 'glass' && (
                        <div style={{ marginBottom: '12px' }}>
                          <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框效果</label>
                          <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                              <input
                                type="radio"
                                name={`noteBgStyle-${comp.id}`}
                                defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                                onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                                style={{ cursor: 'pointer' }}
                              />
                              毛玻璃
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                              <input
                                type="radio"
                                name={`noteBgStyle-${comp.id}`}
                                defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                                onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                                style={{ cursor: 'pointer' }}
                              />
                              柔边阴影
                            </label>
                          </div>

                          {/* 柔边阴影背景设置 */}
                          {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                            <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                              <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                                {/* 颜色选择器 */}
                                <div style={{ flex: '0 0 60px' }}>
                                  <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                  <input
                                    type="color"
                                    defaultValue={comp?.bgColor || '#ffffff'}
                                    onChange={(e) => debouncedUpdateComponent(comp.id, { bgColor: e.target.value })}
                                    style={{
                                      width: '100%',
                                      height: '36px',
                                      border: tc('borderInput'),
                                      borderRadius: '6px',
                                      cursor: 'pointer',
                                      padding: '2px'
                                    }}
                                  />
                                </div>

                                {/* 透明度滑块 */}
                                <div style={{ flex: 1 }}>
                                  <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                    背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                  </label>
                                  <input
                                    type="range"
                                    min="0"
                                    max="100"
                                    step="5"
                                    defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                    onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                    style={{
                                      width: '100%',
                                      cursor: 'pointer'
                                    }}
                                  />
                                </div>
                                <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                  <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                    <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => debouncedUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                    显示边框
                                  </label>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </>
                  )}

                  {comp.type === 'personal' && (
                    <>
                      <div style={{ marginBottom: '10px', border: '1px solid #e0e0e0', borderRadius: '6px', overflow: 'hidden' }}>
                        <div style={{ padding: '8px 10px', background: tc('bgPanel'), display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', fontSize: '12px', fontWeight: 600, color: tc('textSecondary'), userSelect: 'none' }}>
                            <input
                              type="checkbox"
                              checked={comp.showPersonalInfo !== false}
                              onChange={(e) => {
                                e.stopPropagation();
                                debouncedUpdateComponent(comp.id, { showPersonalInfo: e.target.checked });
                              }}
                              onClick={(e) => e.stopPropagation()}
                              style={{ cursor: 'pointer' }}
                            />
                            展示个人信息
                          </label>
                        </div>
                        <details open style={{}}>
                          <summary style={{ padding: '6px 10px', cursor: 'pointer', fontSize: '11px', fontWeight: 600, color: '#888', listStyle: 'none', display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <span style={{ fontSize: '10px' }}>&#9654;</span> 名字 / 签名 / 头像
                          </summary>
                          <div style={{ padding: '8px 10px' }}>
                            <div style={{ marginBottom: '10px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>名字</label>
                              <input
                                type="text"
                                defaultValue={comp.name}
                                onChange={(e) => { if (comp.showPersonalInfo !== false) debouncedUpdateComponent(comp.id, { name: e.target.value }); }}
                                onClick={(e) => e.stopPropagation()}
                                onFocus={(e) => e.stopPropagation()}
                                disabled={comp.showPersonalInfo === false}
                                style={{
                                  width: '100%',
                                  padding: '8px 12px',
                                  border: tc('borderInput'),
                                  borderRadius: '6px',
                                  fontSize: '14px',
                                  opacity: comp.showPersonalInfo === false ? 0.5 : 1,
                                  cursor: comp.showPersonalInfo === false ? 'not-allowed' : 'text'
                                }}
                              />
                            </div>
                            <div style={{ marginBottom: '10px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>个性签名</label>
                              <input
                                type="text"
                                defaultValue={comp.tagline}
                                onChange={(e) => { if (comp.showPersonalInfo !== false) debouncedUpdateComponent(comp.id, { tagline: e.target.value }); }}
                                onClick={(e) => e.stopPropagation()}
                                onFocus={(e) => e.stopPropagation()}
                                disabled={comp.showPersonalInfo === false}
                                style={{
                                  width: '100%',
                                  padding: '8px 12px',
                                  border: tc('borderInput'),
                                  borderRadius: '6px',
                                  fontSize: '14px',
                                  opacity: comp.showPersonalInfo === false ? 0.5 : 1,
                                  cursor: comp.showPersonalInfo === false ? 'not-allowed' : 'text'
                                }}
                              />
                            </div>
                            <div>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>头像图片地址</label>
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <div style={{ flex: 1, position: 'relative' }}>
                            {(() => {
                              // 验证图片 URL 是否有效
                              const validateAvatarUrl = (url, onSuccess) => {
                                setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));

                                // 创建图片对象进行检测
                                const img = new Image();

                                // 成功加载
                                img.onload = () => {
                                  setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));
                                  onSuccess();
                                };

                                // 加载失败
                                img.onerror = () => {
                                  setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '图片地址不正确' }));
                                };

                                // 开始加载
                                img.src = url;
                              };

                              // 提取图片搜索逻辑为函数
                              const searchAvatarImages = (searchTerm) => {
                                const dropdown = document.getElementById(`avatar-dropdown-${comp.id}`);
                                const list = document.getElementById(`avatar-list-${comp.id}`);

                                if (!dropdown || !list) return;

                                if (searchTerm.length === 0) {
                                  dropdown.style.display = 'none';
                                  return;
                                }

                                list.innerHTML = '';

                                // 检查是否是 http/https URL
                                if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                                  // URL 模式：在下拉列表中显示该 URL
                                  const item = document.createElement('div');
                                  item.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; color: #667eea; font-weight: 500;";
                                  item.textContent = searchTerm;
                                  item.onmousedown = (e) => {
                                    e.preventDefault();
                                    setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));
                                    // 点击后进行检测
                                    validateAvatarUrl(searchTerm, () => {
                                      debouncedUpdateComponent(comp.id, { avatar: searchTerm });
                                    });
                                    dropdown.style.display = 'none';
                                  };
                                  list.appendChild(item);
                                  dropdown.style.display = 'block';
                                  return;
                                }

                                // 本地文件搜索模式
                                // 获取所有图片文件
                                const allFiles = vault.getFiles();
                                const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico', '.avif', '.tiff', '.tif', '.heic', '.heif'];
                                const imageFiles = allFiles.filter(f =>
                                  imageExtensions.some(ext => f.path.toLowerCase().endsWith(ext))
                                );

                                // 模糊匹配
                                const matches = imageFiles.filter(f =>
                                  f.path.toLowerCase().includes(searchTerm)
                                ).slice(0, 10);

                                if (matches.length === 0) {
                                  const noResult = document.createElement('div');
                                  noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                                  noResult.textContent = '未找到匹配的图片';
                                  list.appendChild(noResult);
                                } else {
                                  matches.forEach(match => {
                                    const item = document.createElement('div');
                                    item.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #f0f0f0;";
                                    item.textContent = match.path;
                                    item.onmousedown = (e) => {
                                      e.preventDefault();
                                      const inputEl = document.getElementById(`avatar-src-${comp.id}`);
                                      if (inputEl) {
                                        inputEl.value = match.path;
                                      }
                                      setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));
                                      debouncedUpdateComponent(comp.id, { avatar: match.path });
                                      dropdown.style.display = 'none';
                                    };
                                    list.appendChild(item);
                                  });

                                  dropdown.style.display = 'block';
                                }
                              };

                              return (
                                <>
                                <input
                                  id={`avatar-src-${comp.id}`}
                                  type="text"
                                  defaultValue={comp.avatar || ''}
                                  placeholder="输入图片路径或 URL，留空显示默认头像"
                                  disabled={comp.showPersonalInfo === false}
                                  onClick={(e) => e.stopPropagation()}
                                  onFocus={() => {
                                    const dropdown = document.getElementById(`avatar-dropdown-${comp.id}`);
                                    if (dropdown) dropdown.style.display = 'block';
                                    setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));
                                  }}
                                  onBlur={() => {
                                    setTimeout(() => {
                                      const dropdown = document.getElementById(`avatar-dropdown-${comp.id}`);
                                      if (dropdown) dropdown.style.display = 'none';
                                    }, 200);
                                  }}
                                  onKeyDown={(e) => {
                                    // 回车键确认
                                    if (e.key === 'Enter') {
                                      const url = e.target.value.trim();
                                      if (url) {
                                        if (url.startsWith('http://') || url.startsWith('https://')) {
                                          // URL 模式：先检测再应用
                                          setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));
                                          validateAvatarUrl(url, () => {
                                            debouncedUpdateComponent(comp.id, { avatar: url });
                                          });
                                        } else {
                                          // 本地路径模式：直接应用
                                          setAvatarUrlErrors(prev => ({ ...prev, [comp.id]: '' }));
                                          debouncedUpdateComponent(comp.id, { avatar: url });
                                        }
                                      }
                                      e.currentTarget.blur();
                                    }
                                  }}
                                  onCompositionStart={(e) => {
                                    e.target.dataset.isComposing = 'true';
                                  }}
                                  onCompositionEnd={(e) => {
                                    e.target.dataset.isComposing = 'false';
                                    const url = e.target.value.trim();
                                    if (url) {
                                      searchAvatarImages(url.toLowerCase());
                                    }
                                  }}
                                  onInput={(e) => {
                                    const url = e.target.value.trim();
                                    if (e.target.dataset.isComposing === 'true') return;
                                    searchAvatarImages(url.toLowerCase());
                                  }}
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '14px'
                                  }}
                                />
                                {avatarUrlErrors[comp.id] && (
                                  <div style={{
                                    color: tc('errorText'),
                                    fontSize: '11px',
                                    marginTop: '4px'
                                  }}>
                                    {avatarUrlErrors[comp.id]}
                                  </div>
                                )}
                                </>
                              );
                            })()}
                            {/* 搜索结果下拉框 */}
                            <div
                              id={`avatar-dropdown-${comp.id}`}
                              style={{
                                display: 'none',
                                position: 'absolute',
                                top: '100%',
                                left: 0,
                                right: 0,
                                background: tc('bgInput'),
                                border: tc('borderInput'),
                                borderRadius: '6px',
                                boxShadow: tc('shadowPopup'),
                                zIndex: 100,
                                maxHeight: '200px',
                                overflowY: 'auto',
                                marginTop: '4px'
                              }}
                            >
                              <div id={`avatar-list-${comp.id}`}></div>
                            </div>
                          </div>

                          {/* 上传按钮 */}
                          <button
                            disabled={comp.showPersonalInfo === false}
                            onClick={() => {
                              const input = document.createElement('input');
                              input.type = 'file';
                              input.accept = 'image/*';
                              input.onchange = async (e) => {
                                const file = e.target.files?.[0];
                                if (!file) return;

                                try {
                                  // 生成唯一文件名
                                  const timestamp = Date.now();
                                  const ext = file.name.split('.').pop() || 'png';
                                  const fileName = `avatar_${timestamp}.${ext}`;

                                  // 使用 Obsidian API 获取附件保存路径（根据用户设置的附件默认存放路径）
                                  const filePath = await app.fileManager.getAvailablePathForAttachment(fileName, currentFilePath);

                                  // 读取文件内容
                                  const arrayBuffer = await file.arrayBuffer();

                                  // 创建文件
                                  await vault.createBinary(filePath, arrayBuffer);

                                  // 更新输入框和组件配置
                                  const inputEl = document.getElementById(`avatar-src-${comp.id}`);
                                  if (inputEl) {
                                    inputEl.value = filePath;
                                  }
                                  debouncedUpdateComponent(comp.id, { avatar: filePath });
                                } catch (error) {
                                  console.error('上传失败:', error);
                                  console.error('上传失败:', error.message);
                                }
                              };
                              input.click();
                            }}
                            style={{
                              padding: '8px 16px',
                              background: '#667eea',
                              border: 'none',
                              borderRadius: '6px',
                              color: '#fff',
                              fontSize: '13px',
                              cursor: 'pointer',
                              whiteSpace: 'nowrap'
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.background = '#5568d3'}
                            onMouseLeave={(e) => e.currentTarget.style.background = '#667eea'}
                          >
                            上传
                          </button>
                        </div>
                        <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                          支持外部 URL、Obsidian 路径或上传图片
                        </div>
                      </div>
                    </div>
                  </details>
                </div>
                      <details style={{ marginBottom: '10px', border: '1px solid #e0e0e0', borderRadius: '6px', overflow: 'hidden' }}>
                        <summary style={{ padding: '8px 10px', background: tc('bgPanel'), cursor: 'pointer', fontSize: '12px', fontWeight: 600, color: tc('textSecondary'), listStyle: 'none', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span style={{ fontSize: '10px' }}>&#9654;</span> ✏️ 文字样式设置
                        </summary>
                        <div style={{ padding: '8px 10px' }}>
                          <div style={{ fontSize: '11px', fontWeight: 600, color: '#888', marginBottom: '6px' }}>名字</div>
                          <div style={{ display: 'flex', gap: '8px', marginBottom: '10px' }}>
                            <div style={{ flex: '0 0 70px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: '#888', marginBottom: '2px' }}>字号</label>
                              <input type="number" defaultValue={comp.nameFontSize || 24}
                                onChange={(e) => debouncedUpdateComponent(comp.id, { nameFontSize: parseInt(e.target.value) || 24 })}
                                onClick={(e) => e.stopPropagation()} onFocus={(e) => e.stopPropagation()}
                                style={{ width: '100%', padding: '6px 10px', border: tc('borderInput'), borderRadius: '6px', fontSize: '13px' }} />
                            </div>
                            <div style={{ flex: '0 0 80px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: '#888', marginBottom: '2px' }}>颜色</label>
                              <input type="color" defaultValue={comp.nameColor || '#333f4f'}
                                onChange={(e) => debouncedUpdateComponent(comp.id, { nameColor: e.target.value })}
                                style={{ width: '100%', height: '30px', border: tc('borderInput'), borderRadius: '6px', cursor: 'pointer', padding: '2px' }} />
                            </div>
                          </div>
                          <div style={{ fontSize: '11px', fontWeight: 600, color: '#888', marginBottom: '6px' }}>个性签名</div>
                          <div style={{ display: 'flex', gap: '8px', marginBottom: '4px' }}>
                            <div style={{ flex: '0 0 70px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: '#888', marginBottom: '2px' }}>字号</label>
                              <input type="number" defaultValue={comp.taglineFontSize || 14}
                                onChange={(e) => debouncedUpdateComponent(comp.id, { taglineFontSize: parseInt(e.target.value) || 14 })}
                                onClick={(e) => e.stopPropagation()} onFocus={(e) => e.stopPropagation()}
                                style={{ width: '100%', padding: '6px 10px', border: tc('borderInput'), borderRadius: '6px', fontSize: '13px' }} />
                            </div>
                            <div style={{ flex: '0 0 80px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: '#888', marginBottom: '2px' }}>颜色</label>
                              <input type="color" defaultValue={comp.taglineColor || '#35bfab'}
                                onChange={(e) => debouncedUpdateComponent(comp.id, { taglineColor: e.target.value })}
                                style={{ width: '100%', height: '30px', border: tc('borderInput'), borderRadius: '6px', cursor: 'pointer', padding: '2px' }} />
                            </div>
                          </div>
                          <div style={{ fontSize: '11px', fontWeight: 600, color: '#888', marginBottom: '6px' }}>菜单</div>
                          <div style={{ display: 'flex', gap: '8px', marginBottom: '4px' }}>
                            <div style={{ flex: '0 0 80px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: '#888', marginBottom: '2px' }}>颜色</label>
                              <input type="color" defaultValue={comp.menuFontColor || '#7b888e'}
                                onChange={(e) => debouncedUpdateComponent(comp.id, { menuFontColor: e.target.value })}
                                style={{ width: '100%', height: '30px', border: tc('borderInput'), borderRadius: '6px', cursor: 'pointer', padding: '2px' }} />
                            </div>
                          </div>
                        </div>
                      </details>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>菜单项</label>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', paddingRight: '8px', maxHeight: '300px', overflowY: 'auto' }}>
                          {(comp.menuItems || []).map((item, idx) => (
                            <div key={idx} style={{ border: tc('borderInput'), borderRadius: '8px', padding: '8px', background: tc('bgPanel') }}>
                              <div style={{ display: 'flex', gap: '6px', alignItems: 'center', marginBottom: '8px' }}>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    const newMenuItems = [...(comp.menuItems || [])];
                                    if (idx > 0) {
                                      [newMenuItems[idx - 1], newMenuItems[idx]] = [newMenuItems[idx], newMenuItems[idx - 1]];
                                      debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                    }
                                  }}
                                  disabled={idx === 0}
                                  style={{
                                    width: '24px',
                                    height: '24px',
                                    padding: 0,
                                    background: idx === 0 ? 'rgba(0,0,0,0.05)' : tc('accentBg'),
                                    border: 'none',
                                    borderRadius: '4px',
                                    color: '#fff',
                                    fontSize: '14px',
                                    cursor: idx === 0 ? 'not-allowed' : 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    flexShrink: 0
                                  }}
                                  title="上移"
                                >
                                  ↑
                                </button>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    const newMenuItems = [...(comp.menuItems || [])];
                                    if (idx < newMenuItems.length - 1) {
                                      [newMenuItems[idx], newMenuItems[idx + 1]] = [newMenuItems[idx + 1], newMenuItems[idx]];
                                      debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                    }
                                  }}
                                  disabled={idx === (comp.menuItems || []).length - 1}
                                  style={{
                                    width: '24px',
                                    height: '24px',
                                    padding: 0,
                                    background: idx === (comp.menuItems || []).length - 1 ? 'rgba(0,0,0,0.05)' : tc('accentBg'),
                                    border: 'none',
                                    borderRadius: '4px',
                                    color: '#fff',
                                    fontSize: '14px',
                                    cursor: idx === (comp.menuItems || []).length - 1 ? 'not-allowed' : 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    flexShrink: 0
                                  }}
                                  title="下移"
                                >
                                  ↓
                                </button>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    const newMenuItems = (comp.menuItems || []).filter((_, i) => i !== idx);
                                    debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                  }}
                                  style={{
                                    width: '24px',
                                    height: '24px',
                                    padding: 0,
                                    background: `linear-gradient(135deg, #f093fb 0%, ${tc('dangerColor')} 100%)`,
                                    border: 'none',
                                    borderRadius: '4px',
                                    color: '#fff',
                                    fontSize: '14px',
                                    cursor: 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    flexShrink: 0
                                  }}
                                  title="删除"
                                >
                                  ×
                                </button>
                                <select
                                  value={item.openTarget || 'mini'}
                                  onClick={(e) => e.stopPropagation()}
                                  onChange={(e) => {
                                    e.stopPropagation();
                                    const newMenuItems = [...(comp.menuItems || [])];
                                    newMenuItems[idx] = { ...newMenuItems[idx], openTarget: e.target.value };
                                    debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                  }}
                                  style={{
                                    padding: '4px 6px',
                                    border: tc('borderInput'),
                                    borderRadius: '4px',
                                    fontSize: '11px',
                                    height: '24px',
                                    flexShrink: 0,
                                    backgroundColor: tc('bgInput'),
                                    cursor: 'pointer'
                                  }}
                                >
                                  <option value="mini">迷你面板</option>
                                  <option value="tab">新标签页</option>
                                </select>
                              </div>
                              <div style={{ display: 'flex', gap: '6px', marginBottom: '6px' }}>
                                <input
                                  type="text"
                                  defaultValue={item.label}
                                  onClick={(e) => e.stopPropagation()}
                                  onChange={(e) => {
                                    const newMenuItems = [...(comp.menuItems || [])];
                                    newMenuItems[idx] = { ...newMenuItems[idx], label: e.target.value };
                                    debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                  }}
                                  placeholder="标签"
                                  style={{
                                    flex: 1,
                                    padding: '6px 10px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '13px',
                                    backgroundColor: tc('bgInput')
                                  }}
                                />
                                <select
                                  value={item.icon}
                                  onChange={(e) => {
                                    const newMenuItems = [...(comp.menuItems || [])];
                                    newMenuItems[idx] = { ...newMenuItems[idx], icon: e.target.value };
                                    debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                  }}
                                  style={{
                                    padding: '6px 4px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '16px',
                                    width: '50px',
                                    textAlign: 'center',
                                    height: '34px',
                                    flexShrink: 0,
                                    backgroundColor: tc('bgInput')
                                  }}
                                >
                                  <option value="file-text">📄</option>
                                  <option value="folder">📁</option>
                                  <option value="home">🏠</option>
                                  <option value="search">🔍</option>
                                  <option value="settings">⚙️</option>
                                  <option value="star">⭐</option>
                                  <option value="heart">❤️</option>
                                  <option value="bookmark">🔖</option>
                                  <option value="calendar">📅</option>
                                  <option value="clock">🕐</option>
                                  <option value="check-circle">✅</option>
                                  <option value="circle">⭕</option>
                                  <option value="code">💻</option>
                                  <option value="database">🗄️</option>
                                  <option value="download">⬇️</option>
                                  <option value="external-link">🔗</option>
                                  <option value="eye">👁️</option>
                                  <option value="filter">🔬</option>
                                  <option value="globe">🌐</option>
                                  <option value="hash">#️⃣</option>
                                  <option value="image">🖼️</option>
                                  <option value="info">ℹ️</option>
                                  <option value="link">🔗</option>
                                  <option value="list">📋</option>
                                  <option value="lock">🔒</option>
                                  <option value="mail">📧</option>
                                  <option value="map">🗺️</option>
                                  <option value="menu">☰</option>
                                  <option value="more-horizontal">⋯</option>
                                  <option value="music">🎵</option>
                                  <option value="paperclip">📎</option>
                                  <option value="play">▶️</option>
                                  <option value="plus">➕</option>
                                  <option value="power">🔌</option>
                                  <option value="refresh">🔄</option>
                                  <option value="save">💾</option>
                                  <option value="share">📤</option>
                                  <option value="shield">🛡️</option>
                                  <option value="smile">😊</option>
                                  <option value="tag">🏷️</option>
                                  <option value="target">🎯</option>
                                  <option value="trash">🗑️</option>
                                  <option value="upload">⬆️</option>
                                  <option value="user">👤</option>
                                  <option value="video">🎬</option>
                                  <option value="zap">⚡</option>
                                  <option value="chevron-right">›</option>
                                  <option value="chevron-down">⌄</option>
                                  <option value="arrow-right">→</option>
                                  <option value="arrow-left">←</option>
                                  <option value="arrow-up">↑</option>
                                  <option value="arrow-down">↓</option>
                                </select>
                              </div>
                              <div>
                                <div style={{ display: 'flex', gap: '8px', marginBottom: '4px' }}>
                                  <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', cursor: 'pointer' }}>
                                    <input
                                      type="radio"
                                      name={`linkMode-${comp.id}-${idx}`}
                                      defaultChecked={(item.linkMode || 'link') === 'link'}
                                      onChange={() => {
                                        const newMenuItems = [...(comp.menuItems || [])];
                                        newMenuItems[idx] = { ...newMenuItems[idx], linkMode: 'link' };
                                        debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                      }}
                                      style={{ cursor: 'pointer' }}
                                    />
                                    链接
                                  </label>
                                  <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', cursor: 'pointer' }}>
                                    <input
                                      type="radio"
                                      name={`linkMode-${comp.id}-${idx}`}
                                      defaultChecked={(item.linkMode || 'link') === 'command'}
                                      onChange={() => {
                                        const newMenuItems = [...(comp.menuItems || [])];
                                        newMenuItems[idx] = { ...newMenuItems[idx], linkMode: 'command' };
                                        debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                      }}
                                      style={{ cursor: 'pointer' }}
                                    />
                                    命令
                                  </label>
                                </div>
                                {(item.linkMode || 'link') === 'link' ? (
                                  (() => {
                                    const linkInputId = `menu-link-input-${comp.id}-${idx}`;
                                    const dropdownId = `menu-link-dropdown-${comp.id}-${idx}`;
                                    const listId = `menu-link-list-${comp.id}-${idx}`;

                                    // 提取文件搜索逻辑
                                    const searchFiles = (searchTerm) => {
                                      const dropdown = document.getElementById(dropdownId);
                                      const list = document.getElementById(listId);

                                      if (!dropdown || !list) return;

                                      // 如果是 URL，不显示搜索结果
                                      if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                                        dropdown.style.display = 'none';
                                        return;
                                      }

                                      if (searchTerm.length === 0) {
                                        dropdown.style.display = 'none';
                                        return;
                                      }

                                      // 获取所有文件
                                      const allFiles = vault.getFiles();

                                      // 模糊匹配文件路径（支持所有文件类型）
                                      const matches = allFiles.filter(f =>
                                        f.path.toLowerCase().includes(searchTerm)
                                      ).slice(0, 10);

                                      list.innerHTML = '';

                                      if (matches.length === 0) {
                                        const noResult = document.createElement('div');
                                        noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                                        noResult.textContent = '未找到匹配的文件';
                                        list.appendChild(noResult);
                                      } else {
                                        matches.forEach(match => {
                                          const itemEl = document.createElement('div');
                                          itemEl.style.cssText =
                                            "padding: 8px 12px;" +
                                            "cursor: pointer;" +
                                            "font-size: 12px;" +
                                            `border-bottom: ${tc('borderSubtle')};`;
                                          itemEl.textContent = match.path;
                                          itemEl.onmousedown = (e) => {
                                            e.preventDefault();
                                            const inputEl = document.getElementById(linkInputId);
                                            if (inputEl) {
                                              inputEl.value = match.path;
                                            }
                                            const newMenuItems = [...(comp.menuItems || [])];
                                            newMenuItems[idx] = { ...newMenuItems[idx], link: match.path };
                                            debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                            dropdown.style.display = 'none';
                                          };
                                          list.appendChild(itemEl);
                                        });

                                        dropdown.style.display = 'block';
                                      }
                                    };

                                    return (
                                      <div style={{ position: 'relative' }}>
                                        <input
                                          id={linkInputId}
                                          type="text"
                                          defaultValue={item.link || ''}
                                          onClick={(e) => e.stopPropagation()}
                                          onFocus={() => {
                                            const dropdown = document.getElementById(dropdownId);
                                            if (dropdown) dropdown.style.display = 'block';
                                          }}
                                          onBlur={() => {
                                            setTimeout(() => {
                                              const dropdown = document.getElementById(dropdownId);
                                              if (dropdown) dropdown.style.display = 'none';
                                            }, 200);
                                          }}
                                          onCompositionStart={(e) => {
                                            e.target.dataset.isComposing = 'true';
                                          }}
                                          onCompositionEnd={(e) => {
                                            e.target.dataset.isComposing = 'false';
                                            const newMenuItems = [...(comp.menuItems || [])];
                                            newMenuItems[idx] = { ...newMenuItems[idx], link: e.target.value };
                                            debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                            searchFiles(e.target.value.toLowerCase());
                                          }}
                                          onInput={(e) => {
                                            if (e.target.dataset.isComposing === 'true') return;
                                            const newMenuItems = [...(comp.menuItems || [])];
                                            newMenuItems[idx] = { ...newMenuItems[idx], link: e.target.value };
                                            debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                            searchFiles(e.target.value.toLowerCase());
                                          }}
                                          placeholder="链接地址或搜索文件..."
                                          style={{
                                            width: '100%',
                                            padding: '6px 10px',
                                            border: tc('borderInput'),
                                            borderRadius: '6px',
                                            fontSize: '13px',
                                            backgroundColor: tc('bgInput')
                                          }}
                                        />
                                        {/* 搜索结果下拉框 */}
                                        <div
                                          id={dropdownId}
                                          style={{
                                            display: 'none',
                                            position: 'absolute',
                                            top: '100%',
                                            left: 0,
                                            right: 0,
                                            background: tc('bgInput'),
                                            border: tc('borderInput'),
                                            borderRadius: '6px',
                                            boxShadow: tc('shadowPopup'),
                                            zIndex: 100,
                                            maxHeight: '180px',
                                            overflowY: 'auto',
                                            marginTop: '4px'
                                          }}
                                        >
                                          <div id={listId}></div>
                                        </div>
                                      </div>
                                    );
                                  })()
                                ) : (
                                  (() => {
                                    const inputId = `cmd-input-${comp.id}-${idx}`;
                                    const dropdownId = `cmd-dropdown-${comp.id}-${idx}`;
                                    const listId = `cmd-list-${comp.id}-${idx}`;

                                    // 获取已保存的命令名称
                                    const commandsResult = commands.listCommands();
                                    const allCommands = Array.isArray(commandsResult) ? commandsResult : [];
                                    const savedCommandId = item.commandId || '';
                                    const savedCommand = allCommands.find(c => c.id === savedCommandId);
                                    const initialValue = savedCommand?.name || '';

                                    return (
                                      <div style={{ position: 'relative' }}>
                                        <input
                                          id={inputId}
                                          type="text"
                                          defaultValue={initialValue}
                                          onClick={(e) => e.stopPropagation()}
                                          onFocus={(e) => {
                                            const dropdown = document.getElementById(dropdownId);
                                            if (dropdown) dropdown.style.display = 'block';
                                          }}
                                          onBlur={() => {
                                            setTimeout(() => {
                                              const dropdown = document.getElementById(dropdownId);
                                              if (dropdown) dropdown.style.display = 'none';
                                            }, 200);
                                          }}
                                          onInput={(e) => {
                                            const searchTerm = e.target.value;
                                            const dropdown = document.getElementById(dropdownId);
                                            const list = document.getElementById(listId);

                                            if (!dropdown || !list) return;

                                            if (searchTerm.length === 0) {
                                              dropdown.style.display = 'none';
                                              return;
                                            }

                                            // 过滤命令
                                            const filteredCommands = allCommands
                                              .filter(cmd => cmd.name && cmd.name.toLowerCase().includes(searchTerm.toLowerCase()))
                                              .slice(0, 20);

                                            list.innerHTML = '';

                                            if (filteredCommands.length === 0) {
                                              const noResult = document.createElement('div');
                                              noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                                              noResult.textContent = '未找到匹配的命令';
                                              list.appendChild(noResult);
                                            } else {
                                              filteredCommands.forEach(cmd => {
                                                const itemEl = document.createElement('div');
                                                itemEl.style.cssText =
                                                  "padding: 8px 12px;" +
                                                  "cursor: pointer;" +
                                                  "font-size: 12px;" +
                                                  `border-bottom: ${tc('borderSubtle')};` +
                                                  `background: ${cmd.id === savedCommandId ? tc('accentSubtle') : tc('bgInput')};`;
                                                itemEl.textContent = cmd.name;
                                                itemEl.onmousedown = (e) => {
                                                  e.preventDefault();
                                                  const inputEl = document.getElementById(inputId);
                                                  if (inputEl) {
                                                    inputEl.value = cmd.name;
                                                  }
                                                  const newMenuItems = [...(comp.menuItems || [])];
                                                  newMenuItems[idx] = { ...newMenuItems[idx], commandId: cmd.id };
                                                  debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                                                  dropdown.style.display = 'none';
                                                };
                                                itemEl.onmouseenter = function() {
                                                  this.style.background = tc('bgHover');
                                                };
                                                itemEl.onmouseleave = function() {
                                                  this.style.background = cmd.id === savedCommandId ? tc('accentSubtle') : tc('bgInput');
                                                };
                                                list.appendChild(itemEl);
                                              });
                                            }

                                            dropdown.style.display = 'block';
                                          }}
                                          placeholder="搜索命令..."
                                          style={{
                                            width: '100%',
                                            padding: '6px 10px',
                                            border: tc('borderInput'),
                                            borderRadius: '6px',
                                            fontSize: '13px',
                                            backgroundColor: tc('bgInput')
                                          }}
                                        />
                                        {/* 搜索结果下拉框 */}
                                        <div
                                          id={dropdownId}
                                          style={{
                                            display: 'none',
                                            position: 'absolute',
                                            top: '100%',
                                            left: 0,
                                            right: 0,
                                            background: tc('bgInput'),
                                            border: tc('borderInput'),
                                            borderRadius: '6px',
                                            boxShadow: tc('shadowPopup'),
                                            zIndex: 100,
                                            maxHeight: '180px',
                                            overflowY: 'auto',
                                            marginTop: '4px'
                                          }}
                                        >
                                          <div id={listId}></div>
                                        </div>
                                        {savedCommand && (
                                          <div style={{ fontSize: '10px', color: tc('successText'), marginTop: '2px' }}>
                                            ✓ 已选择
                                          </div>
                                        )}
                                      </div>
                                    );
                                  })()
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                        <button
                          onClick={() => {
                            const newMenuItems = [...(comp.menuItems || []), { label: '新项目', icon: 'blog', link: '', linkMode: 'link', commandId: '' }];
                            debouncedUpdateComponent(comp.id, { menuItems: newMenuItems });
                          }}
                          style={{
                            padding: '8px 16px',
                            background: tc('accent'),
                            border: 'none',
                            borderRadius: '8px',
                            color: '#fff',
                            fontSize: '13px',
                            cursor: 'pointer',
                            width: '100%',
                            marginTop: '4px'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.background = tc('accentHover')}
                          onMouseLeave={(e) => e.currentTarget.style.background = tc('accent')}
                        >
                          + 添加菜单项
                        </button>
                      </div>

                      {/* 外框样式设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`personalBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                              style={{ cursor: 'pointer' }}
                            />
                            毛玻璃
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`personalBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                              style={{ cursor: 'pointer' }}
                            />
                            柔边阴影
                          </label>
                        </div>

                        {/* 柔边阴影背景设置 */}
                        {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                              {/* 颜色选择器 */}
                              <div style={{ flex: '0 0 60px' }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                <input
                                  type="color"
                                  defaultValue={comp?.bgColor || '#ffffff'}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgColor: e.target.value })}
                                  style={{
                                    width: '100%',
                                    height: '36px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    padding: '2px'
                                  }}
                                />
                              </div>

                              {/* 透明度滑块 */}
                              <div style={{ flex: 1 }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                  背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                </label>
                                <input
                                  type="range"
                                  min="0"
                                  max="100"
                                  step="5"
                                  defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                  style={{
                                    width: '100%',
                                    cursor: 'pointer'
                                  }}
                                />
                              </div>
                              <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                  <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => debouncedUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                  显示边框
                                </label>
                              </div>
                            </div>
                            <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                              <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                            </div>
                          </div>
                        )}
                        {(comp?.backgroundStyle || 'glass') === 'glass' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                            <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                          </div>
                        )}
                      </div>
                    </>
                  )}

                  {comp.type === 'kanban' && (
                    <>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题</label>
                        <input
                          type="text"
                          defaultValue={comp.title}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>
                      <div style={{ marginBottom: '12px', display: 'flex', gap: '16px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showTitle !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { showTitle: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示标题
                        </label>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showAddColumnBtn !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { showAddColumnBtn: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示添加列按钮
                        </label>
                      </div>
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={!!comp.maxHeight}
                            onChange={(e) => {
                              if (e.target.checked) {
                                debouncedUpdateComponent(comp.id, { maxHeight: comp.maxHeight || '300px' });
                              } else {
                                debouncedUpdateComponent(comp.id, { maxHeight: '' });
                              }
                            }}
                            style={{ cursor: 'pointer' }}
                          />
                          限制最大高度
                        </label>
                        <div style={{ marginTop: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <input
                            id={`kanban-maxheight-${comp.id}`}
                            type="text"
                            placeholder="请输入正整数，例如 300"
                            defaultValue={comp.maxHeight ? parseInt(comp.maxHeight) : ''}
                            disabled={!comp.maxHeight}
                            onKeyPress={(e) => {
                              // 只允许输入数字
                              if (!/\d/.test(e.key)) e.preventDefault();
                            }}
                            style={{
                              flex: 1,
                              padding: '6px 10px',
                              border: tc('borderInput'),
                              borderRadius: '4px',
                              fontSize: '13px',
                              opacity: !comp.maxHeight ? 0.4 : 1
                            }}
                          />
                          <button
                            disabled={!comp.maxHeight}
                            onClick={() => {
                              const input = document.getElementById(`kanban-maxheight-${comp.id}`);
                              if (input) {
                                const num = parseInt(input.value);
                                if (num > 0 && num <= 99999) {
                                  input.value = num;
                                  debouncedUpdateComponent(comp.id, { maxHeight: num + 'px' });
                                }
                              }
                            }}
                            style={{
                              padding: '6px 12px',
                              background: comp.maxHeight ? '#667eea' : '#ddd',
                              color: '#fff',
                              border: 'none',
                              borderRadius: '4px',
                              fontSize: '12px',
                              cursor: comp.maxHeight ? 'pointer' : 'not-allowed',
                              whiteSpace: 'nowrap'
                            }}
                          >
                            确定
                          </button>
                        </div>
                      </div>
                      <div style={{ padding: '8px 12px', background: tc('accentSubtle'), borderRadius: '6px', fontSize: '11px', color: tc('accent'), lineHeight: '1.5' }}>
                        💡 看板使用说明：<br/>
                        • 拖拽卡片可在列之间移动<br/>
                        • 双击卡片可编辑内容，按 Enter 换行，失去焦点保存<br/>
                        • 双击列标题可编辑列名<br/>
                        • 右键看板区域：添加列、切换背景显示<br/>
                        • 右键卡片：删除卡片、设置背景颜色<br/>
                        • 右键列区域：删除列、设置背景颜色<br/>
                        • 点击"+添加卡片"添加任务卡片
                      </div>

                      {/* 外框样式设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`kanbanBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                              style={{ cursor: 'pointer' }}
                            />
                            毛玻璃
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`kanbanBgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                              onChange={() => debouncedUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                              style={{ cursor: 'pointer' }}
                            />
                            柔边阴影
                          </label>
                        </div>

                        {/* 柔边阴影背景设置 */}
                        {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                              {/* 颜色选择器 */}
                              <div style={{ flex: '0 0 60px' }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                <input
                                  type="color"
                                  defaultValue={comp?.bgColor || '#ffffff'}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgColor: e.target.value })}
                                  style={{
                                    width: '100%',
                                    height: '36px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    padding: '2px'
                                  }}
                                />
                              </div>

                              {/* 透明度滑块 */}
                              <div style={{ flex: 1 }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                  背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                </label>
                                <input
                                  type="range"
                                  min="0"
                                  max="100"
                                  step="5"
                                  defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                  style={{
                                    width: '100%',
                                    cursor: 'pointer'
                                  }}
                                />
                              </div>
                              <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                  <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => debouncedUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                  显示边框
                                </label>
                              </div>
                            </div>
                            <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                              <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                            </div>
                          </div>
                        )}
                        {(comp?.backgroundStyle || 'glass') === 'glass' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                            <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                          </div>
                        )}
                      </div>
                    </>
                  )}

                  {comp.type === 'spacer' && (
                    <div style={{ marginBottom: '12px' }}>
                      <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>间距高度</label>
                      <input
                        type="number"
                        defaultValue={comp.height}
                        onChange={(e) => debouncedUpdateComponent(comp.id, { height: parseInt(e.target.value) })}
                        style={{
                          width: '100%',
                          padding: '8px 12px',
                          border: tc('borderInput'),
                          borderRadius: '6px',
                          fontSize: '14px'
                        }}
                      />
                    </div>
                  )}

                  {comp.type === 'image' && (
                    <>
                      {/* 图片地址输入框（支持模糊搜索） */}
                      <div style={{ marginBottom: '12px', position: 'relative' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>图片地址</label>
                        <div style={{ display: 'flex', gap: '8px' }}>
                          <div style={{ flex: 1, position: 'relative' }}>
                            {(() => {
                              // 提取图片搜索逻辑
                              const searchImageFiles = (searchTerm) => {
                                const dropdown = document.getElementById(`image-dropdown-${comp.id}`);
                                const list = document.getElementById(`image-list-${comp.id}`);

                                if (!dropdown || !list) return;

                                // 如果是 URL 格式，不显示下拉搜索
                                if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                                  dropdown.style.display = 'none';
                                  return;
                                }

                                if (searchTerm.length === 0) {
                                  dropdown.style.display = 'none';
                                  return;
                                }

                                // 获取所有图片文件
                                const allFiles = vault.getFiles();
                                const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico', '.avif', '.tiff', '.tif', '.heic', '.heif'];
                                const imageFiles = allFiles.filter(f =>
                                  imageExtensions.some(ext => f.path.toLowerCase().endsWith(ext))
                                );

                                // 模糊匹配
                                const matches = imageFiles.filter(f =>
                                  f.path.toLowerCase().includes(searchTerm)
                                ).slice(0, 10);

                                if (matches.length === 0) {
                                  dropdown.style.display = 'none';
                                  return;
                                }

                                // 渲染下拉列表
                                list.innerHTML = '';
                                matches.forEach(file => {
                                  const item = document.createElement('div');
                                  item.style.cssText = 'padding: 8px 12px; cursor: pointer; font-size: 12px; display: flex; align-items: center; gap: 8px;';
                                  item.onmouseenter = () => item.style.background = tc('accentSubtle');
                                  item.onmouseleave = () => item.style.background = 'transparent';

                                  const icon = document.createElement('span');
                                  icon.textContent = '🖼️';
                                  icon.style.fontSize = '14px';

                                  const text = document.createElement('span');
                                  text.textContent = file.path;
                                  text.style.cssText = 'flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;';

                                  item.appendChild(icon);
                                  item.appendChild(text);

                                  item.onclick = () => {
                                    const input = document.getElementById(`image-src-${comp.id}`);
                                    if (input) {
                                      input.value = file.path;
                                      debouncedUpdateComponent(comp.id, { src: file.path });
                                    }
                                    dropdown.style.display = 'none';
                                  };

                                  list.appendChild(item);
                                });

                                dropdown.style.display = 'block';
                              };

                              // 验证并应用图片路径
                              const validateAndApplyImage = (value) => {
                                const src = value.trim();
                                if (!src) {
                                  debouncedUpdateComponent(comp.id, { src: '' });
                                  return;
                                }

                                if (src.startsWith('http://') || src.startsWith('https://')) {
                                  // URL 模式：直接应用（不验证，因为CORS会导致验证失败）
                                  debouncedUpdateComponent(comp.id, { src: src });
                                } else {
                                  // 本地路径模式：验证文件是否存在
                                  const file = vault.getAbstractFileByPath(src);
                                  if (file) {
                                    debouncedUpdateComponent(comp.id, { src: src });
                                  } else {
                                    // 文件不存在，延迟重试（等待文件索引更新）
                                    setTimeout(() => {
                                      const retryFile = vault.getAbstractFileByPath(src);
                                      if (retryFile) {
                                        debouncedUpdateComponent(comp.id, { src: src });
                                      }
                                    }, 500);
                                  }
                                }
                              };

                              return (
                                <input
                                  id={`image-src-${comp.id}`}
                                  type="text"
                                  defaultValue={comp.src || ''}
                                  placeholder="输入图片路径或 URL，回车确认"
                                  onFocus={() => {
                                    const dropdown = document.getElementById(`image-dropdown-${comp.id}`);
                                    if (dropdown) dropdown.style.display = 'block';
                                  }}
                                  onBlur={() => {
                                    setTimeout(() => {
                                      const dropdown = document.getElementById(`image-dropdown-${comp.id}`);
                                      if (dropdown) dropdown.style.display = 'none';
                                    }, 200);
                                  }}
                                  onKeyDown={(e) => {
                                    if (e.key === 'Enter') {
                                      validateAndApplyImage(e.target.value);
                                      e.currentTarget.blur();
                                    }
                                  }}
                                  onCompositionStart={(e) => {
                                    e.target.dataset.isComposing = 'true';
                                  }}
                                  onCompositionEnd={(e) => {
                                    e.target.dataset.isComposing = 'false';
                                    const value = e.target.value;
                                    searchImageFiles(value.toLowerCase());
                                  }}
                                  onInput={(e) => {
                                    if (e.target.dataset.isComposing === 'true') return;
                                    const value = e.target.value;
                                    searchImageFiles(value.toLowerCase());
                                  }}
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '14px'
                                  }}
                                />
                              );
                            })()}
                            {/* 搜索结果下拉框 */}
                            <div
                              id={`image-dropdown-${comp.id}`}
                              style={{
                                display: 'none',
                                position: 'absolute',
                                top: '100%',
                                left: 0,
                                right: 0,
                                background: tc('bgInput'),
                                border: tc('borderInput'),
                                borderRadius: '6px',
                                boxShadow: tc('shadowPopup'),
                                zIndex: 100,
                                maxHeight: '200px',
                                overflowY: 'auto',
                                marginTop: '4px'
                              }}
                            >
                              <div id={`image-list-${comp.id}`}></div>
                            </div>
                          </div>

                          {/* 上传按钮 */}
                          <button
                            onClick={() => {
                              const input = document.createElement('input');
                              input.type = 'file';
                              input.accept = 'image/*';
                              input.onchange = async (e) => {
                                const file = e.target.files?.[0];
                                if (!file) return;

                                try {
                                  // 生成唯一文件名
                                  const timestamp = Date.now();
                                  const ext = file.name.split('.').pop() || 'png';
                                  const fileName = `image_${timestamp}.${ext}`;

                                  // 使用 Obsidian API 获取附件保存路径（根据用户设置的附件默认存放路径）
                                  const filePath = await app.fileManager.getAvailablePathForAttachment(fileName, currentFilePath);

                                  // 读取文件内容
                                  const arrayBuffer = await file.arrayBuffer();

                                  // 创建文件
                                  await vault.createBinary(filePath, arrayBuffer);

                                  // 更新输入框
                                  const inputEl = document.getElementById(`image-src-${comp.id}`);
                                  if (inputEl) {
                                    inputEl.value = filePath;
                                  }

                                  // 延迟更新组件配置，确保文件索引已更新
                                  await new Promise(resolve => setTimeout(resolve, 300));
                                  debouncedUpdateComponent(comp.id, { src: filePath });

                                  console.log('✓ 图片上传成功！');
                                } catch (err) {
                                  console.error('上传失败:', err);
                                  console.error('图片上传失败: ' + err.message);
                                }
                              };
                              input.click();
                            }}
                            style={{
                              padding: '8px 12px',
                              background: '#667eea',
                              border: 'none',
                              borderRadius: '6px',
                              color: '#fff',
                              fontSize: '12px',
                              cursor: 'pointer',
                              whiteSpace: 'nowrap',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px'
                            }}
                            title="上传本地图片"
                          >
                            📤 上传
                          </button>
                        </div>
                        <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                          支持仓库路径或URL（以http/https开头，按回车确认）
                        </div>
                      </div>

                      {/* 标题/说明文字 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showTitle !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { showTitle: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示标题/说明文字
                        </label>
                      </div>
                      {comp.showTitle !== false && (
                        <>
                          <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题内容</label>
                            <input
                              type="text"
                              defaultValue={comp.title || ''}
                              placeholder="图片标题"
                              onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                              onClick={(e) => e.stopPropagation()}
                              onFocus={(e) => e.stopPropagation()}
                              style={{
                                width: '100%',
                                padding: '8px 12px',
                                border: tc('borderInput'),
                                borderRadius: '6px',
                                fontSize: '14px'
                              }}
                            />
                          </div>
                          <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题位置</label>
                            <select
                              defaultValue={comp.captionPosition || 'bottom'}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { captionPosition: e.target.value })}
                              style={{
                                width: '100%',
                                padding: '12px 14px',
                                border: tc('borderInput'),
                                borderRadius: '6px',
                                fontSize: '13px',
                                minHeight: '44px'
                              }}
                            >
                              <option value="top">顶部</option>
                              <option value="bottom">底部</option>
                            </select>
                          </div>
                        </>
                      )}

                      {/* 图片链接设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.enableLink || false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { enableLink: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          启用图片链接
                        </label>
                      </div>

                      {comp.enableLink && (
                        <>
                          {/* 链接模式选择 */}
                          <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '6px' }}>链接模式</label>
                            <div style={{ display: 'flex', gap: '16px' }}>
                              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                                <input
                                  type="radio"
                                  name={`imageLinkMode-${comp.id}`}
                                  defaultChecked={(comp?.linkMode || 'link') === 'link'}
                                  onChange={() => debouncedUpdateComponent(comp.id, { linkMode: 'link' })}
                                  style={{ cursor: 'pointer' }}
                                />
                                链接
                              </label>
                              <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                                <input
                                  type="radio"
                                  name={`imageLinkMode-${comp.id}`}
                                  defaultChecked={(comp?.linkMode || 'link') === 'command'}
                                  onChange={() => debouncedUpdateComponent(comp.id, { linkMode: 'command' })}
                                  style={{ cursor: 'pointer' }}
                                />
                                命令
                              </label>
                            </div>
                          </div>

                          {/* 链接输入 */}
                          {(comp?.linkMode || 'link') === 'link' ? (
                        (() => {
                          const linkInputId = `image-link-input-${comp.id}`;
                          const dropdownId = `image-link-dropdown-${comp.id}`;
                          const listId = `image-link-list-${comp.id}`;

                          // 文件搜索逻辑
                          const searchFiles = (searchTerm) => {
                            const dropdown = document.getElementById(dropdownId);
                            const list = document.getElementById(listId);

                            if (!dropdown || !list) return;

                            // 如果是 URL，不显示搜索结果
                            if (searchTerm.startsWith('http://') || searchTerm.startsWith('https://')) {
                              dropdown.style.display = 'none';
                              return;
                            }

                            if (searchTerm.length === 0) {
                              dropdown.style.display = 'none';
                              return;
                            }

                            // 获取所有文件
                            const allFiles = app.vault.getFiles();

                            // 模糊匹配文件路径（支持所有文件类型）
                            const matches = allFiles.filter(f =>
                              f.path.toLowerCase().includes(searchTerm)
                            ).slice(0, 10);

                            list.innerHTML = '';

                            if (matches.length === 0) {
                              const noResult = document.createElement('div');
                              noResult.style.cssText = `padding: 8px 12px; color: ${tc('textLabel')}; font-size: 12px;`;
                              noResult.textContent = '未找到匹配的文件';
                              list.appendChild(noResult);
                            } else {
                              matches.forEach(match => {
                                const itemEl = document.createElement('div');
                                itemEl.style.cssText = "padding: 8px 12px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #f0f0f0;";
                                itemEl.textContent = match.path;
                                itemEl.onmousedown = (e) => {
                                  e.preventDefault();
                                  const inputEl = document.getElementById(linkInputId);
                                  if (inputEl) {
                                    inputEl.value = match.path;
                                  }
                                  const newValue = match.path;
                                  setLinkInputState({
                                    value: newValue,
                                    currentComponentId: comp.id
                                  });
                                  debouncedUpdateComponent(comp.id, { link: newValue });
                                  dropdown.style.display = 'none';
                                };
                                list.appendChild(itemEl);
                              });

                              dropdown.style.display = 'block';
                            }
                          };

                          return (
                            <div style={{ marginBottom: '12px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>链接地址</label>
                              <div style={{ position: 'relative' }}>
                                <input
                                  key={`link-input-${comp.id}`}
                                  id={linkInputId}
                                  type="text"
                                  value={linkInputState.currentComponentId === comp.id ? linkInputState.value : (comp?.link || '')}
                                  onClick={(e) => e.stopPropagation()}
                                  onFocus={(e) => {
                                    // 初始化或重置链接输入状态
                                    if (linkInputState.currentComponentId !== comp.id) {
                                      setLinkInputState({
                                        value: comp?.link || '',
                                        currentComponentId: comp.id
                                      });
                                    }
                                    const dropdown = document.getElementById(dropdownId);
                                    if (dropdown) dropdown.style.display = 'block';
                                  }}
                                  onBlur={() => {
                                    setTimeout(() => {
                                      const dropdown = document.getElementById(dropdownId);
                                      if (dropdown) dropdown.style.display = 'none';
                                    }, 200);
                                  }}
                                  onCompositionStart={(e) => {
                                    e.target.dataset.isComposing = 'true';
                                  }}
                                  onCompositionEnd={(e) => {
                                    e.target.dataset.isComposing = 'false';
                                    const newValue = e.target.value;
                                    setLinkInputState(prev => ({ ...prev, value: newValue }));
                                    debouncedUpdateComponent(comp.id, { link: newValue });
                                    searchFiles(newValue.toLowerCase());
                                  }}
                                  onInput={(e) => {
                                    if (e.target.dataset.isComposing === 'true') return;
                                    const newValue = e.target.value;
                                    setLinkInputState(prev => ({ ...prev, value: newValue }));
                                    debouncedUpdateComponent(comp.id, { link: newValue });
                                    searchFiles(newValue.toLowerCase());
                                  }}
                                  placeholder="https://example.com 或 搜索文件..."
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '14px'
                                  }}
                                />
                                {/* 搜索结果下拉框 */}
                                <div
                                  id={dropdownId}
                                  style={{
                                    display: 'none',
                                    position: 'absolute',
                                    top: '100%',
                                    left: 0,
                                    right: 0,
                                    background: tc('bgInput'),
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    boxShadow: tc('shadowPopup'),
                                    zIndex: 100,
                                    maxHeight: '180px',
                                    overflowY: 'auto',
                                    marginTop: '4px'
                                  }}
                                >
                                  <div id={listId}></div>
                                </div>
                              </div>
                              <div style={{ fontSize: '11px', color: tc('textLabel'), marginTop: '4px' }}>
                                支持外部 URL（https://...）或 搜索选择文件
                              </div>
                            </div>
                          );
                        })()
                      ) : (
                        (() => {
                          // 命令模式：搜索并选择命令
                          const commandsResult = commands.listCommands();
                          const allCommands = Array.isArray(commandsResult) ? commandsResult : [];
                          const savedCommandId = comp?.commandId || '';
                          const savedCommand = allCommands.find(c => c.id === savedCommandId);

                          // 检测组件变化，重置状态
                          if (commandSelectorState.currentComponentId !== comp.id) {
                            setCommandSelectorState({
                              searchQuery: '',
                              showList: false,
                              isComposing: false,
                              currentComponentId: comp.id,
                              isUserEditing: false
                            });
                          }

                          // 简单的命令过滤（不使用 useMemo）
                          let filteredCommands = allCommands.slice(0, 20);
                          if (commandSelectorState.searchQuery.trim() && !commandSelectorState.isComposing) {
                            const search = commandSelectorState.searchQuery.toLowerCase();
                            filteredCommands = allCommands
                              .filter(cmd => cmd.name.toLowerCase().includes(search))
                              .slice(0, 20);
                          }

                          return (
                            <div style={{ marginBottom: '12px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>选择命令</label>
                              <div style={{ position: 'relative' }}>
                                <input
                                  type="text"
                                  value={commandSelectorState.isUserEditing ? commandSelectorState.searchQuery : (commandSelectorState.searchQuery || savedCommand?.name || '')}
                                  onChange={(e) => {
                                    setCommandSelectorState(prev => ({ ...prev, searchQuery: e.target.value, isUserEditing: true }));
                                    if (!commandSelectorState.isComposing) {
                                      setCommandSelectorState(prev => ({ ...prev, showList: true }));
                                    }
                                  }}
                                  onCompositionStart={() => setCommandSelectorState(prev => ({ ...prev, isComposing: true }))}
                                  onCompositionEnd={(e) => {
                                    setCommandSelectorState(prev => ({ ...prev, isComposing: false, searchQuery: e.target.value, showList: true }));
                                  }}
                                  onFocus={(e) => {
                                    e.stopPropagation();
                                    setCommandSelectorState(prev => ({
                                      ...prev,
                                      showList: true,
                                      searchQuery: '',
                                      isUserEditing: true
                                    }));
                                  }}
                                  onBlur={() => {
                                    // 延迟隐藏，以便点击事件能够触发
                                    setTimeout(() => setCommandSelectorState(prev => ({ ...prev, showList: false, isUserEditing: false })), 200);
                                  }}
                                  placeholder="搜索命令..."
                                  onClick={(e) => e.stopPropagation()}
                                  onMouseDown={(e) => e.stopPropagation()}
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    fontSize: '14px'
                                  }}
                                />
                                {commandSelectorState.showList && filteredCommands.length > 0 && (
                                  <div style={{
                                    position: 'absolute',
                                    top: '100%',
                                    left: 0,
                                    right: 0,
                                    maxHeight: '200px',
                                    overflowY: 'auto',
                                    background: tc('bgInput'),
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    marginTop: '4px',
                                    boxShadow: tc('shadowPopup'),
                                    zIndex: 10
                                  }}>
                                    {filteredCommands.map(cmd => (
                                      <div
                                        key={cmd.id}
                                        onClick={(e) => {
                                          e.stopPropagation();
                                          setCommandSelectorState(prev => ({ ...prev, searchQuery: cmd.name, showList: false, isUserEditing: false }));
                                          debouncedUpdateComponent(comp.id, { commandId: cmd.id });
                                        }}
                                        onMouseDown={(e) => e.preventDefault()}
                                        style={{
                                          padding: '10px 12px',
                                          cursor: 'pointer',
                                          borderBottom: `1px solid #f0f0f0`,
                                          fontSize: '13px',
                                          background: cmd.id === savedCommandId ? tc('accentSubtle') : '#fff'
                                        }}
                                        onMouseEnter={(e) => {
                                          e.currentTarget.style.background = tc('bgHover');
                                        }}
                                        onMouseLeave={(e) => {
                                          e.currentTarget.style.background = cmd.id === savedCommandId ? tc('accentSubtle') : '#fff';
                                        }}
                                      >
                                        {cmd.name}
                                      </div>
                                    ))}
                                  </div>
                                )}
                                {savedCommand && !commandSelectorState.isUserEditing && (
                                  <div style={{ fontSize: '11px', color: tc('successText'), marginTop: '4px' }}>
                                    ✓ 已选择: {savedCommand.name}
                                  </div>
                                )}
                              </div>
                            </div>
                          );
                        })()
                      )}
                        </>
                      )}

                      {/* 对象适应方式 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>图片适应方式</label>
                        <select
                          defaultValue={comp.objectFit || 'cover'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { objectFit: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '12px 14px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '13px',
                            minHeight: '44px'
                          }}
                        >
                          <option value="cover">裁剪填充（cover）</option>
                          <option value="contain">完整显示（contain）</option>
                          <option value="fill">拉伸填充（fill）</option>
                          <option value="none">原始大小（none）</option>
                        </select>
                      </div>

                      {/* 边框设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.border?.enabled !== false}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { border: { ...comp.border, enabled: e.target.checked } })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示边框
                        </label>
                      </div>

                      {comp.border?.enabled !== false && (
                        <>
                          <div style={{ marginBottom: '12px' }}>
                            <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>边框样式</label>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '6px' }}>
                              {[
                                { id: 'none', name: '无边框', icon: '⬜' },
                                { id: 'rounded', name: '圆角', icon: '🔲' },
                                { id: 'circle', name: '圆形', icon: '⭕' },
                                { id: 'square', name: '矩形', icon: '▫️' }
                              ].map(style => (
                                <button
                                  key={style.id}
                                  onClick={() => debouncedUpdateComponent(comp.id, { border: { ...comp.border, style: style.id } })}
                                  style={{
                                    padding: '10px 8px',
                                    background: (comp?.border?.style || 'rounded') === style.id ? tc('accentBg') : '#f5f5f5',
                                    border: (comp?.border?.style || 'rounded') === style.id ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                                    borderRadius: '6px',
                                    fontSize: '12px',
                                    cursor: 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '4px'
                                  }}
                                >
                                  {style.icon} {style.name}
                                </button>
                              ))}
                            </div>
                          </div>

                          {comp.border?.style === 'rounded' && (
                            <div style={{ marginBottom: '12px' }}>
                              <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>圆角大小</label>
                              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                                <input
                                  type="range"
                                  min="0"
                                  max="50"
                                  defaultValue={comp.border?.radius || 12}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { border: { ...comp.border, radius: parseInt(e.target.value) } })}
                                  style={{ flex: 1 }}
                                />
                                <span style={{ fontSize: '12px', color: tc('textSecondary'), minWidth: '30px' }}>{comp.border?.radius || 12}px</span>
                              </div>
                            </div>
                          )}

                          {comp.border?.style !== 'none' && (
                            <>
                              <div style={{ marginBottom: '12px' }}>
                                <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>边框宽度</label>
                                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                                  <input
                                    type="range"
                                    min="1"
                                    max="10"
                                    defaultValue={comp.border?.width || 3}
                                    onChange={(e) => debouncedUpdateComponent(comp.id, { border: { ...comp.border, width: parseInt(e.target.value) } })}
                                    style={{ flex: 1 }}
                                  />
                                  <span style={{ fontSize: '12px', color: tc('textSecondary'), minWidth: '30px' }}>{comp.border?.width || 3}px</span>
                                </div>
                              </div>

                              <div style={{ marginBottom: '12px' }}>
                                <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>边框颜色</label>
                                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                                  <input
                                    type="color"
                                    defaultValue={comp.border?.color || '#ffffff'}
                                    onChange={(e) => debouncedUpdateComponent(comp.id, { border: { ...comp.border, color: e.target.value } })}
                                    style={{
                                      width: '40px',
                                      height: '36px',
                                      border: tc('borderInput'),
                                      borderRadius: '6px',
                                      cursor: 'pointer',
                                      padding: '2px'
                                    }}
                                  />
                                  <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                                    {['transparent', '#ffffff', '#000000', '#667eea', '#f5576c', '#48bb78', '#f6ad55'].map(color => (
                                      <button
                                        key={color}
                                        onClick={() => debouncedUpdateComponent(comp.id, { border: { ...comp.border, color } })}
                                        style={{
                                          width: '24px',
                                          height: '24px',
                                          background: color === 'transparent' ? 'linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%), linear-gradient(45deg, #ccc 25%, transparent 25%, transparent 75%, #ccc 75%)' : color,
                                          backgroundSize: '8px 8px',
                                          backgroundPosition: '0 0, 4px 4px',
                                          border: comp?.border?.color === color ? tc('kanbanEditBorder') : tc('kanbanColBorder'),
                                          borderRadius: '4px',
                                          cursor: 'pointer'
                                        }}
                                        title={color === 'transparent' ? '无色' : color}
                                      />
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </>
                          )}
                        </>
                      )}

                      {/* 阴影 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>阴影效果</label>
                        <select
                          defaultValue={comp.shadow || 'medium'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { shadow: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '12px 14px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '13px',
                            minHeight: '44px'
                          }}
                        >
                          <option value="none">无阴影</option>
                          <option value="small">小阴影</option>
                          <option value="medium">中等阴影</option>
                          <option value="large">大阴影</option>
                          <option value="glow">发光效果</option>
                        </select>
                      </div>

                      {/* 透明度 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>透明度</label>
                        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                          <input
                            type="range"
                            min="0"
                            max="100"
                            defaultValue={comp.opacity || 100}
                            onChange={(e) => debouncedUpdateComponent(comp.id, { opacity: parseInt(e.target.value) })}
                            style={{ flex: 1 }}
                          />
                          <span style={{ fontSize: '12px', color: tc('textSecondary'), minWidth: '35px' }}>{comp.opacity || 100}%</span>
                        </div>
                      </div>

                      {/* 滤镜效果 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>滤镜效果</label>
                        <select
                          defaultValue={comp.filter || 'none'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { filter: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '12px 14px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '13px',
                            minHeight: '44px',
                            marginBottom: '8px'
                          }}
                        >
                          <option value="none">无滤镜</option>
                          <option value="grayscale">灰度</option>
                          <option value="blur">模糊</option>
                          <option value="brightness">亮度</option>
                          <option value="contrast">对比度</option>
                          <option value="saturate">饱和度</option>
                          <option value="sepia">复古</option>
                          <option value="invert">反色</option>
                        </select>
                        {comp.filter && comp.filter !== 'none' && (
                          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                            <input
                              type="range"
                              min="0"
                              max="200"
                              defaultValue={comp.filterValue || 100}
                              onChange={(e) => debouncedUpdateComponent(comp.id, { filterValue: parseInt(e.target.value) })}
                              style={{ flex: 1 }}
                            />
                            <span style={{ fontSize: '12px', color: tc('textSecondary'), minWidth: '35px' }}>{comp.filterValue || 100}%</span>
                          </div>
                        )}
                      </div>

                      {/* 悬停效果 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>悬停效果</label>
                        <select
                          defaultValue={comp.hoverEffect || 'zoom'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { hoverEffect: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '12px 14px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '13px',
                            minHeight: '44px'
                          }}
                        >
                          <option value="none">无效果</option>
                          <option value="zoom">放大</option>
                          <option value="lift">上浮</option>
                          <option value="rotate">旋转</option>
                        </select>
                      </div>

                      {/* 使用提示 */}
                      <div style={{ padding: '8px 12px', background: tc('accentSubtle'), borderRadius: '6px', fontSize: '11px', color: tc('accent'), lineHeight: '1.5' }}>
                        💡 图片组件使用提示：<br/>
                        • 支持仓库内图片路径和外部 URL<br/>
                        • 输入路径时会自动搜索匹配的图片<br/>
                        • 点击「上传」按钮可直接上传本地图片<br/>
                        • 圆形样式适合头像图片
                      </div>
                    </>
                  )}

                  {comp.type === 'sidebar' && (
                    <>
                      {/* 标题设置 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '4px' }}>标题</label>
                        <input
                          type="text"
                          defaultValue={comp.title || '侧边栏'}
                          onChange={(e) => debouncedUpdateComponent(comp.id, { title: e.target.value })}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: tc('borderInput'),
                            borderRadius: '6px',
                            fontSize: '14px'
                          }}
                        />
                      </div>

                      {/* 显示标题开关 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showTitle !== false}
                            onChange={(e) => immediateUpdateComponent(comp.id, { showTitle: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示标题
                        </label>
                      </div>

                      {/* 显示视图按钮开关 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: tc('textSecondary') }}>
                          <input
                            type="checkbox"
                            defaultChecked={comp.showButtons !== false}
                            onChange={(e) => immediateUpdateComponent(comp.id, { showButtons: e.target.checked })}
                            style={{ cursor: 'pointer' }}
                          />
                          显示视图选择按钮
                        </label>
                      </div>

                      {/* 外框样式 */}
                      <div style={{ marginBottom: '12px' }}>
                        <label style={{ display: 'block', fontSize: '12px', color: tc('textSecondary'), marginBottom: '8px' }}>外框样式</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '8px', flexWrap: 'wrap' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`bgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'glass'}
                              onChange={() => immediateUpdateComponent(comp.id, { backgroundStyle: 'glass' })}
                              style={{ cursor: 'pointer' }}
                            />
                            毛玻璃
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', cursor: 'pointer' }}>
                            <input
                              type="radio"
                              name={`bgStyle-${comp.id}`}
                              defaultChecked={(comp?.backgroundStyle || 'glass') === 'softShadow'}
                              onChange={() => immediateUpdateComponent(comp.id, { backgroundStyle: 'softShadow' })}
                              style={{ cursor: 'pointer' }}
                            />
                            柔边阴影
                          </label>
                        </div>

                        {/* 柔边阴影设置 */}
                        {(comp?.backgroundStyle || 'glass') === 'softShadow' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                              {/* 自定义调色板 */}
                              <div style={{ flex: '0 0 60px' }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>背景颜色</label>
                                <input
                                  type="color"
                                  defaultValue={comp?.bgColor || '#ffffff'}
                                  onChange={(e) => immediateUpdateComponent(comp.id, { bgColor: e.target.value })}
                                  style={{
                                    width: '100%',
                                    height: '36px',
                                    border: tc('borderInput'),
                                    borderRadius: '6px',
                                    cursor: 'pointer',
                                    padding: '2px'
                                  }}
                                />
                              </div>

                              {/* 透明度滑块 */}
                              <div style={{ flex: 1 }}>
                                <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>
                                  背景透明度: {Math.round((comp?.bgOpacity ?? 0.9) * 100)}%
                                </label>
                                <input
                                  type="range"
                                  min="0"
                                  max="100"
                                  step="5"
                                  defaultValue={Math.round((comp?.bgOpacity ?? 0.9) * 100)}
                                  onChange={(e) => debouncedUpdateComponent(comp.id, { bgOpacity: parseInt(e.target.value) / 100 })}
                                  style={{
                                    width: '100%',
                                    cursor: 'pointer'
                                  }}
                                />
                              </div>
                              <div style={{ flex: '0 0 auto', alignSelf: 'center' }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: tc('textSecondary'), cursor: 'pointer', whiteSpace: 'nowrap' }}>
                                  <input type="checkbox" defaultChecked={comp?.showBorder !== false} onChange={(e) => immediateUpdateComponent(comp.id, { showBorder: e.target.checked })} />
                                  显示边框
                                </label>
                              </div>
                            </div>
                            <div style={{ marginTop: '12px', borderTop: tc('borderSubtle'), paddingTop: '12px' }}>
                              <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                              <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                            </div>
                          </div>
                        )}
                        {(comp?.backgroundStyle || 'glass') === 'glass' && (
                          <div style={{ marginTop: '12px', padding: '12px', background: tc('bgPanel'), borderRadius: '6px' }}>
                            <label style={{ display: 'block', fontSize: '11px', color: tc('textSecondary'), marginBottom: '6px' }}>圆角大小: {comp?.borderRadius ?? 24}px</label>
                            <input type="range" min="0" max="48" step="4" defaultValue={comp?.borderRadius ?? 24} onChange={(e) => debouncedUpdateComponent(comp.id, { borderRadius: parseInt(e.target.value) })} style={{ width: '100%', cursor: 'pointer' }} />
                          </div>
                        )}
                      </div>

                      {/* 使用提示 */}
                      <div style={{ padding: '8px 12px', background: tc('accentSubtle'), borderRadius: '6px', fontSize: '11px', color: tc('accent'), lineHeight: '1.5' }}>
                        💡 侧边栏组件使用提示：<br/>
                        • 自动读取左右侧边栏的视图<br/>
                        • 点击三角形符号可折叠/展开按钮列表<br/>
                        • 支持反向链接、大纲等所有侧边栏视图<br/>
                        • 内容区域支持上下滚动<br/>
                        • ✨ 会自动记住上次选择的视图和折叠状态
                      </div>
                    </>
                  )}
                </div>
              );
            })()}

            <div style={{ display: 'flex', gap: '8px', marginTop: '20px' }}>
              <button
                onClick={() => { flushPendingUpdates(); setEditingComponent(null); }}
                style={{
                  flex: 1,
                  padding: '10px',
                  background: '#667eea',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff',
                  fontSize: '14px',
                  cursor: 'pointer'
                }}
              >
                完成
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 主内容区域 */}
      {viewMode ? (
        // 查看模式：显示 mini 主面板和临时 Markdown 卡片
        <div
          data-markdown-card-container="true"
          style={{
            flex: 1,
            overflow: 'visible',
            position: 'relative',
            zIndex: 1
          }}
        >
          {/* Mini 主面板 */}
          {renderMiniNavbar()}

          {/* 临时 Markdown 卡片 */}
          {(() => {
            const cardSettings = getMarkdownCardSettings(viewingPersonalComponentId, currentViewingFile);
            const isDragging = markdownCardDragState.draggingId &&
              markdownCardDragState.draggingId.personalCompId === viewingPersonalComponentId &&
              markdownCardDragState.draggingId.link === currentViewingFile;
            const isResizing = markdownCardDragState.resizingId &&
              markdownCardDragState.resizingId.personalCompId === viewingPersonalComponentId &&
              markdownCardDragState.resizingId.link === currentViewingFile;

            // 使用缓存的调整手柄样式
            const resizeHandles = isEditing ? (
              <>
                <div className="ph-rs-r" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleMarkdownCardResizeStart(e, viewingPersonalComponentId, currentViewingFile, 'right'); }} />
                <div className="ph-rs-b" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleMarkdownCardResizeStart(e, viewingPersonalComponentId, currentViewingFile, 'bottom'); }} />
                <div className="ph-rs-br" data-resize-handle="true" onMouseDown={(e) => { e.stopPropagation(); handleMarkdownCardResizeStart(e, viewingPersonalComponentId, currentViewingFile, 'bottom-right'); }} />
              </>
            ) : null;

            return (
              <div
                className="temp-markdown-card"
                onMouseDown={(e) => {
                  if (isEditing && !e.target.dataset.resizeHandle && !e.target.closest('[data-resize-handle]')) {
                    handleMarkdownCardDragStart(e, viewingPersonalComponentId, currentViewingFile);
                  }
                }}
                style={{
                  position: 'absolute',
                  left: cardSettings.x + 'px',
                  top: cardSettings.y + 'px',
                  width: cardSettings.width + 'px',
                  height: cardSettings.height + 'px',
                  background: tc('cardBgHeavy'),
                  backdropFilter: 'blur(10px)',
                  borderRadius: '24px',
                  boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
                  padding: '32px',
                  overflowY: 'auto',
                  zIndex: 10000,
                  animation: 'fadeInScale 0.3s ease-out forwards',
                  cursor: isEditing ? 'move' : 'default',
                  userSelect: isEditing ? 'none' : 'auto',
                  transition: isDragging || isResizing ? 'none' : 'all 0.2s'
                }}
              >
                <style>{ "@keyframes fadeInScale {" +
                  "  from { opacity: 0; transform: scale(0.95); }" +
                  "  to { opacity: 1; transform: scale(1); }" +
                  "}" +
                  ".temp-markdown-card {" +
                  "  white-space: pre-line !important;" +
                  "  word-wrap: break-word !important;" +
                  "  line-height: 1.8 !important;" +
                  "}" +
                  ".temp-markdown-card * {" +
                  "  white-space: pre-line !important;" +
                  "}" }</style>

                {resizeHandles}

                <Markdown content={`![[${currentViewingFile}]]`} />
              </div>
            );
          })()}
        </>
      ) : (
        // 正常模式：显示所有组件
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '80px 0 40px',
            position: 'relative',
            zIndex: 1
          }}
        >
          <div
            style={{
              position: 'relative',
              minHeight: '400px',
              padding: '0'
            }}
            data-component-container="true"
          >
            {currentConfig.components.length === 0 ? (
              <div style={{
                textAlign: 'center',
                padding: '60px 20px',
                color: 'rgba(255,255,255,0.8)'
              }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>👋</div>
                <h2 style={{ margin: '0 0 8px 0', fontSize: '24px' }}>欢迎使用</h2>
                <p style={{ margin: 0, fontSize: '14px', opacity: 0.8, textAlign: 'center' }}>
                  点击右上角的⚙️按钮开始定制你的主页<br />作者：uuq007
                </p>
              </div>
            ) : (
              <div style={{
                position: 'relative',
                width: '100%',
                height: '100%',
                minHeight: '400px'
              }}>
                {currentConfig.components.map(comp => (
                  <div
                    key={comp.id}
                    data-component-id={comp.id}
                    onMouseDown={(e) => {
                      if (isEditing && !resizingId && !e.target.dataset.resizeHandle) {
                        handleDragStart(e, comp.id);
                      }
                    }}
                    style={{ position: 'absolute' }}
                  >
                    {renderComponent(comp)}
                  </div>
                ))}
                {/* 对齐基准线 */}
                {isEditing && (
                  <div className="ph-guide-ct" data-guide-container="true">
                    {guideLines.vertical.map((pos, idx) => (
                      <div
                        key={`v-${idx}`}
                        style={{
                          position: 'absolute',
                          left: pos + 'px',
                          top: 0,
                          height: '100%',
                          width: '1px',
                          background: '#ff6b6b'
                        }}
                      />
                    ))}
                    {guideLines.horizontal.map((pos, idx) => (
                      <div
                        key={`h-${idx}`}
                        style={{
                          position: 'absolute',
                          top: pos + 'px',
                          left: 0,
                          width: '100%',
                          height: '1px',
                          background: '#ff6b6b'
                        }}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* 编辑模式提示 */}
      {isEditing && (
        <div style={{
          position: 'fixed',
          bottom: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'rgba(102, 126, 234, 0.9)',
          color: '#fff',
          padding: '10px 20px',
          borderRadius: '24px',
          fontSize: '13px',
          zIndex: 10000,
          pointerEvents: 'none'
        }}>
          拖拽组件移动 • 拖拽边缘调整大小 • 点击「页面设置」添加组件
        </div>
      )}
      </>}
    </div>
  );
}

return { EditableHomepage };
```
