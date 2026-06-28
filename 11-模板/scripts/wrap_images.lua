--[[
wrap_images.lua v4 — Pandoc Lua filter
Wrap every image in a figure[H] with centering.
Width by image type (all reduced for compact layout).
Caption from following *italic* text.

Width rules:
  - hydrogen_emission: 0.6\textwidth (line spectrum needs visibility)
  - excalidraw-: 0.5\textwidth
  - .matrix/.flowchart/.decision/.relation/.comparison: 0.45\textwidth
  - radial / 11-19 / 11-20 / 11-13 / 11-21 / 11-22: 0.45\textwidth
  - atomic_radius / ionization / electronegativity / causal-chain: 0.45\textwidth
  - orbital_2p / orbital_3d / orbital_density: 0.45\textwidth
  - default: 0.5\textwidth
]]

local function img_width(src)
  local w = '0.45\\textwidth'  -- default
  if src:match('hydrogen_emission') then
    w = '0.6\\textwidth'
  elseif src:match('excalidraw%-') then
    w = '0.45\\textwidth'
  elseif src:match('%.matrix%.') or src:match('%.flowchart%.') or src:match('%.decision%.')
      or src:match('%.relation%.') or src:match('%.comparison%.') or src:match('%.causal%-chain%.') then
    w = '0.5\\textwidth'  -- 矩阵/流程/因果链图稍大
  elseif src:match('radial') or src:match('11%-19') or src:match('11%-20') or src:match('11%-13') then
    w = '0.45\\textwidth'
  elseif src:match('atomic_radius') or src:match('ionization') or src:match('electronegativity') then
    w = '0.45\\textwidth'
  elseif src:match('orbital_2p') or src:match('orbital_3d') or src:match('orbital_density') or src:match('11%-21') or src:match('11%-22') then
    w = '0.45\\textwidth'
  end
  return w
end

local image_count = 0

function Para(el)
  -- Case 1: Para with only an Image
  if #el.content == 1 and el.content[1].t == 'Image' then
    local img = el.content[1]
    image_count = image_count + 1
    local src = img.src
    local caption_text = ''
    if img.title and img.title ~= '' then
      caption_text = img.title
    end
    local w = img_width(src)
    local caption_part = ''
    if caption_text ~= '' then
      caption_part = '\\caption{' .. caption_text .. '}'
    end
    local latex = '\\begin{figure}[H]\\centering\n'
      .. '\\includegraphics[width=' .. w .. ',keepaspectratio]{' .. src .. '}\n'
      .. caption_part .. '\n'
      .. '\\end{figure}'
    return pandoc.RawBlock('latex', latex)
  end

  -- Case 2: Para with Image + Emph (italic caption)
  if #el.content >= 2 then
    local has_img = false
    local img = nil
    local remaining = {}
    for _, item in ipairs(el.content) do
      if item.t == 'Image' and not has_img then
        has_img = true
        img = item
      else
        table.insert(remaining, item)
      end
    end

    if has_img and img then
      image_count = image_count + 1
      local src = img.src
      local caption_text = ''
      for _, item in ipairs(remaining) do
        if item.t == 'Emph' then
          caption_text = pandoc.utils.stringify(item)
        elseif item.t == 'Str' and img.title and img.title ~= '' then
          caption_text = img.title
        end
      end
      if caption_text == '' and img.title and img.title ~= '' then
        caption_text = img.title
      end
      local w = img_width(src)
      local caption_part = ''
      if caption_text ~= '' then
        caption_part = '\\caption{' .. caption_text .. '}'
      end
      local latex = '\\begin{figure}[H]\\centering\n'
        .. '\\includegraphics[width=' .. w .. ',keepaspectratio]{' .. src .. '}\n'
        .. caption_part .. '\n'
        .. '\\end{figure}'
      return pandoc.RawBlock('latex', latex)
    end
  end

  return nil
end

function Doc(el)
  return nil
end
