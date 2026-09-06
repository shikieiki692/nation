function BlockQuote(el)
  if #el.content > 0 and el.content[1].t == "Para" then
    local first_para = el.content[1]
    if #first_para.content > 0 and first_para.content[1].t == "Str" then
      local first_str = first_para.content[1].text
      
      -- Check if it starts with a callout tag like [!tip]
      local callout_type = first_str:match("^%[%!(%a+)%]$")
      
      if callout_type then
        -- 1. Physical removal for teacher notes
        if callout_type == "teacher" then
          return {} -- Return empty list to remove the block
        end
        
        -- 2. Style mapping
        local style = "Body Text"
        if callout_type == "tip" or callout_type == "info" then
          style = "Methodology Block"
        elseif callout_type == "warning" then
          style = "Mistake Block"
        elseif callout_type == "example" then
          style = "Answer Block"
        end
        
        -- 3. Strip the "[!type]" tag and any immediate spaces
        table.remove(first_para.content, 1)
        while #first_para.content > 0 and (first_para.content[1].t == "Space" or first_para.content[1].t == "SoftBreak") do
          table.remove(first_para.content, 1)
        end
        
        -- 4. Bold the title until the first newline or colon if we want, 
        -- but for now, we just wrap it in a Div with custom-style.
        return pandoc.Div(el.content, pandoc.Attr("", {}, {{"custom-style", style}}))
      end
    end
  end
  return el
end
