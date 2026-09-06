const pptxgen = require('pptxgenjs');
const html2pptx = require('../html2pptx.js');
const path = require('path');

const SLIDES = [
    '01-cover.html', '02-scene.html', '03-everywhere.html', '04-what.html', '05-elements.html',
    '06-think.html', '07-tree.html', '08-tree-big.html', '09-cross.html', '10-element.html',
    '11-allotrope.html', '12-oxide.html', '13-oxide-prop.html', '14-link.html', '15-sure.html',
    '16-acid.html', '17-base.html', '18-salt.html', '19-reaction.html', '20-summary.html',
    '21-ex1.html', '22-ex2.html', '23-ex3.html', '24-ex4.html', '25-ex5.html',
    '26-test12.html', '27-test34.html', '28-test5.html', '29-test6.html', '30-end.html'
];

// 演讲者备注（逐字取自 content-spec.md）
const NOTES = {
    '01-cover.html': '同学们好，今天我们开始高中化学第一章第一节：物质的分类。【1 min】',
    '02-scene.html': '先问学生：图书馆书那么多，为什么你能很快找到？超市也是。答案很简单——分类摆放。化学要研究的物质有数千万种，也需要分类。【1.5 min】',
    '03-everywhere.html': '不只是图书馆和超市——实验室的药品、物流的快递、小区的垃圾分类，分类法无处不在。【1 min】',
    '04-what.html': '给分类下个定义：抓共同点归并，抓差异点区分。分类的关键是先定标准。【1 min】',
    '05-elements.html': '阅读材料：一百多种元素组成数千万种物质。氢、碳、钠、钙、钡各举三个生活例子。物质这么多，不分类没法研究。【2 min】',
    '06-think.html': '试着给这些物质分类。分类没有唯一答案，关键看你选什么标准。高中会把分类标准从宏观拓展到微观。【2 min】',
    '07-tree.html': '第一种方法，树状分类法：像大树分叉，每一级只用一个标准。同层并列，上下层包含。【2 min】',
    '08-tree-big.html': '用树状分类法按组成给刚才的物质分类，结果就是这棵树。注意：NaCl 溶液和 BaSO₄ 浊液是混合物，先被分出去。【2 min】',
    '09-cross.html': '第二种方法，交叉分类法：同一物质从多个角度同时分类。比如 Na₂SO₄，既是钠盐，又是硫酸盐。【2 min】',
    '10-element.html': '思考 1：给单质分类。按元素种类分：金属、非金属、稀有气体。注意同一个元素可能形成好几种单质。【1.5 min】',
    '11-allotrope.html': '同素异形体：同种元素的不同单质。物理性质差异大，相互转化是化学变化。思考题答案：不一定，氧气和臭氧混在一起就是混合物。【2 min】',
    '12-oxide.html': '思考 2：给氧化物分类。按能否成盐、成什么盐来分：酸性、碱性、两性、不成盐四类。【2 min】',
    '13-oxide-prop.html': '酸性氧化物和碱性氧化物的定义里都强调「只生成」。NO₂ 与水反应除酸还生成 NO，Na₂O₂ 与水反应除碱还放氧气，都不符合定义。【2.5 min】',
    '14-link.html': '组成决定性质的大方向：金属氧化物多为碱性，非金属氧化物多为酸性。但只是「大多数」，例外不少。【2 min】',
    '15-sure.html': '四个「一定」辨析，前三个都有反例，只有「碱性氧化物一定是金属氧化物」成立。这是常考易错点。【2 min】',
    '16-acid.html': '思考 3：酸的分类。先给酸下定义——阳离子全部是氢离子。然后四个标准各分一次。【2 min】',
    '17-base.html': '思考 4：碱的分类，模仿酸的标准自己来。定义：阴离子全部是氢氧根。【2 min】',
    '18-salt.html': '思考 5：盐的分类。正盐、酸式盐、碱式盐；也可以按阳离子、阴离子分——那就用上了交叉分类法。【2 min】',
    '19-reaction.html': '反应也能分类。四种基本类型是按物质种类分的；高中还会按电子转移分出氧化还原，按离子分出离子反应——标准不同，分法不同。【2 min】',
    '20-summary.html': '小结：两种分类方法，一个像树一个像网。核心就一句话：分类先定标准。【1 min】',
    '21-ex1.html': '典例 1，按类排队。注意液态氧是纯净的单质，碘酒是溶液即混合物。答案 C。【2 min】',
    '22-ex2.html': '典例 2。易错点：纯碱不是碱是盐，NaHSO₄ 不是酸。答案 B。【2 min】',
    '23-ex3.html': '典例 3，概念间的逻辑关系。注意 D：硫酸和硝酸既是不同酸（并列），又都是含氧酸（交叉）。答案 C。【2 min】',
    '24-ex4.html': '典例 4，交叉分类的应用——阴影处要同时满足两个类别。答案 B。【2.5 min】',
    '25-ex5.html': '典例 5，找不同——角度不同答案可以不同，言之有理即可。第四组有两种合理答案。【2 min】',
    '26-test12.html': '检测 1 答案 C，NaOH 不是钠盐；检测 2 答案 D，碳燃烧可能生成一氧化碳或二氧化碳。【3 min】',
    '27-test34.html': '检测 3 答案 D，CO 等不是酸性氧化物；检测 4 答案 D，A 冰水混合物是纯净物，B NaHSO₄ 是盐，C CO 不是酸性氧化物。【3 min】',
    '28-test5.html': '检测 5 答案 C，D 的 Na₂O₂ 是过氧化物，呼应课上的辨析。【2 min】',
    '29-test6.html': '检测 6：①NaOH 是碱其余是氧化物 ②Al 是金属 ③蒸馏水是纯净物 ④氢气是纯净物 ⑤铜丝是单质。【2 min】',
    '30-end.html': '今天我们学会了给物质分类，下节课看物质之间怎么转化。下课。【0.5 min】'
};

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = '';
    pptx.title = '物质的分类';

    for (const file of SLIDES) {
        const htmlPath = path.join(__dirname, 'slides', file);
        const { slide } = await html2pptx(htmlPath, pptx, { tmpDir: path.join(__dirname, 'tmp') });
        if (NOTES[file]) slide.addNotes(NOTES[file]);
        console.log(`Converted: ${file}`);
    }

    const out = path.join(__dirname, '物质的分类.pptx');
    await pptx.writeFile({ fileName: out });
    console.log('Presentation created:', out);
}

createPresentation().catch((err) => {
    console.error(err);
    process.exit(1);
});
