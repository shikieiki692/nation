--[[
wrap_images.lua v7 — Pandoc Lua filter (reverted: wrapfig removed)
All single images: figure[H] centered (v5 layout).
Multi-image pairs: minipage side-by-side.
Width/height by image type (print-optimized handout layout).
Caption from following *italic* text.
]]

local function img_width(src)
  local w = '0.55\\textwidth'
  if src:match('hydrogen_emission') or src:match('hydrogen%-spectrum') then
    w = '0.70\\textwidth'
  elseif src:match('excalidraw%-') then
    w = '0.60\\textwidth'
  elseif src:match('%.matrix%.') or src:match('%.flowchart%.') or src:match('%.decision%.')
      or src:match('%.relation%.') or src:match('%.comparison%.') or src:match('%.causal%-chain%.') then
    w = '0.68\\textwidth'
  elseif src:match('radial') or src:match('11%-19') or src:match('11%-20') or src:match('11%-13') then
    w = '0.58\\textwidth'
  elseif src:match('atomic_radius') or src:match('ionization') or src:match('electronegativity') then
    w = '0.58\\textwidth'
  elseif src:match('orbital_2p') or src:match('orbital_3d') or src:match('orbital_density') or src:match('orbital%-shapes') or src:match('11%-21') or src:match('11%-22') then
    w = '0.58\\textwidth'
  elseif src:match('构造原理') then
    w = '0.58\\textwidth'
  end
  return w
end

local image_count = 0

local function fit_multi_width(src, total)
  local base = img_width(src)
  if total <= 1 then
    return base
  elseif total == 2 then
    return '0.48\\textwidth'
  else
    return '0.32\\textwidth'
  end
end

local function fit_multi_height(total)
  if total <= 1 then
    return nil
  elseif total == 2 then
    return '0.32\\textheight'
  else
    return '0.24\\textheight'
  end
end

local function trim(text)
  return (text or ''):gsub('^%s+', ''):gsub('%s+$', '')
end

local function basename(src)
  return (src or ''):gsub('^.*[/\\\\]', '')
end

local allowed_pairs = {
  ['puha-13-6a-non-close-packed-layer.jpg|puha-13-6b-close-packed-layer.jpg'] = true,
  ['puha-13-7b-sc-unit-cell.jpg|puha-13-7b-bcc-unit-cell.jpg'] = true,
  ['ccp-unit-cell.jpg|hcp-unit-cell.jpg'] = true,
  ['puha-13-9b-ccp-layer-relation.jpg|puha-13-9b-hcp-layer-relation.jpg'] = true,
  ['puha-13-9c-fcc-unit-cell-from-packing.jpg|puha-13-9c-hex-unit-cell-from-packing.jpg'] = true,
  ['puha-13-8b-tetrahedral-void.jpg|puha-13-8c-octahedral-void.jpg'] = true,
  ['puha-13-11a-nacl.jpg|puha-13-11b-cscl.jpg'] = true,
}

local function normalize_caption(text)
  local original = trim(text)
  local normalized = original:gsub('^图%s*[%d一二三四五六七八九十百零]+[%s:：%.、%-]*', '')
  normalized = trim(normalized)
  if normalized == '' then
    return original
  end
  return normalized
end

local function caption_from_inlines(inlines, fallback)
  local caption_parts = {}
  for _, item in ipairs(inlines) do
    if item.t == 'Emph' then
      local parts = {}
      for _, inline in ipairs(item.content) do
        if inline.t == 'Math' then
          table.insert(parts, '$' .. inline.text .. '$')
        elseif inline.t == 'Str' then
          table.insert(parts, inline.text)
        elseif inline.t == 'Space' or inline.t == 'SoftBreak' then
          table.insert(parts, ' ')
        end
      end
      table.insert(caption_parts, table.concat(parts))
    end
  end

  local caption_text = table.concat(caption_parts)
  if caption_text == '' and fallback and fallback ~= '' then
    caption_text = fallback
  end
  return normalize_caption(caption_text)
end

local function build_figure_latex(images, caption_text)
  local parts = {'\\begin{figure}[H]\\centering'}
  local total = #images
  for idx, img in ipairs(images) do
    local w = fit_multi_width(img.src, total)
    local h = fit_multi_height(total)
    local opts
    if h then
      opts = 'width=' .. w .. ',height=' .. h .. ',keepaspectratio'
    else
      opts = 'width=' .. w .. ',keepaspectratio'
    end
    table.insert(parts, '\\includegraphics[' .. opts .. ']{' .. img.src .. '}')
    if idx < total then
      table.insert(parts, '\\hspace{0.015\\textwidth}')
    end
  end
  if caption_text ~= '' then
    table.insert(parts, '\\caption{' .. caption_text .. '}')
  end
  table.insert(parts, '\\end{figure}')
  return table.concat(parts, '\n')
end

local function build_side_by_side_latex(figs)
  local parts = {'\\begin{center}'}
  for idx, fig in ipairs(figs) do
    local img = fig.images[1]
    table.insert(parts, '\\begin{minipage}[t]{0.48\\textwidth}\\centering')
    table.insert(parts,
      '\\includegraphics[width=0.95\\linewidth,height=0.30\\textheight,keepaspectratio]{' .. img.src .. '}')
    if fig.caption_text ~= '' then
      table.insert(parts, '\\captionof{figure}{' .. fig.caption_text .. '}')
    end
    table.insert(parts, '\\end{minipage}')
    if idx < #figs then
      table.insert(parts, '\\hfill')
    end
  end
  table.insert(parts, '\\end{center}')
  return table.concat(parts, '\n')
end

local function extract_image_para(block)
  if block.t ~= 'Para' then
    return nil
  end

  local images = {}
  local remaining = {}
  for _, item in ipairs(block.content) do
    if item.t == 'Image' then
      table.insert(images, item)
    else
      table.insert(remaining, item)
    end
  end

  if #images == 0 then
    return nil
  end

  image_count = image_count + #images
  return {
    images = images,
    caption_text = caption_from_inlines(remaining, images[1].title),
  }
end

local function can_side_by_side(fig1, fig2)
  if not fig1 or not fig2 then
    return false
  end
  if #fig1.images ~= 1 or #fig2.images ~= 1 then
    return false
  end
  local key = basename(fig1.images[1].src) .. '|' .. basename(fig2.images[1].src)
  return allowed_pairs[key] == true
end

function Pandoc(doc)
  local new_blocks = pandoc.List()
  local i = 1
  while i <= #doc.blocks do
    local fig1 = extract_image_para(doc.blocks[i])
    if fig1 then
      local fig2 = nil
      if i < #doc.blocks then
        fig2 = extract_image_para(doc.blocks[i + 1])
      end

      if can_side_by_side(fig1, fig2) then
        new_blocks:insert(pandoc.RawBlock('latex', build_side_by_side_latex({fig1, fig2})))
        i = i + 2
      else
        new_blocks:insert(pandoc.RawBlock('latex', build_figure_latex(fig1.images, fig1.caption_text)))
        i = i + 1
      end
    else
      new_blocks:insert(doc.blocks[i])
      i = i + 1
    end
  end

  doc.blocks = new_blocks
  return doc
end
