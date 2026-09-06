---
homepage:
  background:
    type: image
    value: "linear-gradient(135deg, #c8d6e5 0%, #62dffe 100%)"
    image: bg_1778769517064.png
    video: ""
  components:
    - id: "1778769820977"
      type: search
      title: 搜索
      placeholder: 搜索笔记...
      width: 350
      height: 335
      maxItems: 10
      x: 350
      y: -80.5
      backgroundStyle: softShadow
      bgOpacity: 0.2
      borderRadius: 0
    - id: "1778769669443"
      type: query
      title: 最近笔记
      queryType: custom
      query: "@page"
      maxItems: 6
      x: 4
      y: 252
      width: 341
      height: 244
      backgroundStyle: softShadow
      bgOpacity: 0.2
      borderRadius: 0
    - id: "1778252820027"
      type: personal
      showPersonalInfo: true
      name: 你的名字
      tagline: 个性签名
      avatar: avatar_1778253253867.jpg
      nameFontSize: 24
      nameColor: "#333f4f"
      nameFontFamily: ""
      taglineFontSize: 14
      taglineColor: "#35bfab"
      taglineFontFamily: ""
      menuFontColor: "#7b888e"
      menuItems:
        - label: 首页
          icon: file-text
          link: 00-首页/首页.md
          linkMode: link
          commandId: ""
          openTarget: mini
        - label: 工作日志
          icon: folder
          link: 00-首页/工作日志.md
          linkMode: link
          commandId: ""
          openTarget: mini
        - label: 使用说明
          icon: smile
          link: 00-首页/使用说明.md
          linkMode: link
          commandId: ""
          openTarget: mini
        - label: 待办
          icon: star
          link: 00-首页/知识库待补充清单.md
          linkMode: link
          commandId: ""
          openTarget: mini
        - label: 自定义项目3
          icon: globe
          link: ""
          linkMode: link
          commandId: ""
          openTarget: mini
      x: -1
      y: -78
      width: 351
      height: 330
      backgroundStyle: softShadow
      bgOpacity: 0.25
      showBorder: false
      borderRadius: 0
---
# 个人主页 v13.4 - 查看器入口

```datacorejsx
const { useState, useEffect, useRef } = dc;

function HomepageLoader() {
  const [Component, setComponent] = useState(null);
  const [status, setStatus] = useState('waiting');
  const loadedRef = useRef(false);
  const retriedRef = useRef(false);

  useEffect(() => {
    if (loadedRef.current) return;
    const dcGlobal = window.datacore;

    const tryLoad = async () => {
      if (loadedRef.current) return;
      loadedRef.current = true;
      setStatus('loading');

      try {
        const mod = await dc.require(dc.headerLink(dc.resolvePath("PersonalHomepageCode.md"), "ViewComponent"));
        setComponent(function() { return mod.EditableHomepage; });
      } catch (e) {
        loadedRef.current = false;
        if (!retriedRef.current) {
          retriedRef.current = true;
          setStatus('reindexing');
          // 查找并执行 DataCore 重建索引命令
          try {
            var cmds = app.commands.commands;
            for (var id in cmds) {
              if (id.indexOf('datacore') !== -1 && cmds[id].name.toLowerCase().indexOf('reindex') !== -1) {
                app.commands.executeCommandById(id);
                break;
              }
            }
          } catch(cmdErr) {}
          // 等待索引完成后重试
          setTimeout(function() { tryLoad(); }, 5000);
        } else {
          setStatus('error');
        }
      }
    };

    if (dcGlobal && dcGlobal.core && dcGlobal.core.initialized) {
      tryLoad();
    } else {
      setStatus('waiting');
      var ref = dcGlobal ? dcGlobal.on("initialized", function() { tryLoad(); }) : null;
      return function() { if (ref && dcGlobal) dcGlobal.offref(ref); };
    }
  }, []);

  if (Component) return <Component />;

  var statusText = status === 'waiting' ? '主页等待索引完成...' :
                   status === 'loading' ? '主页加载中...' :
                   status === 'reindexing' ? '主页加载失败，正在自动重建索引...' :
                   '主页加载失败，请手动执行 DataCore: Reindex entire vault 命令后刷新';

  return <div style={{ padding: 16, color: '#999', fontSize: 13 }}>{statusText}</div>;
}

return <HomepageLoader />;
```
