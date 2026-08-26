const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = '';
    pptx.title = '高中化学课件模板';

    const slides = [
        '01-cover.html',
        '02-usage.html',
        '03-contents.html',
        '04-section.html',
        '05-concept.html',
        '06-points.html',
        '07-cards.html',
        '08-micro.html',
        '09-derivation.html',
        '10-exercise.html',
        '11-lab.html',
        '12-phenomena.html',
        '13-chart.html',
        '14-framework.html',
        '15-quiz.html',
        '16-timeline.html',
        '17-compare.html',
        '18-icons.html',
        '19-blank.html',
        '20-ending.html'
    ];

    for (const file of slides) {
        const htmlPath = path.join(__dirname, 'slides', file);
        const { slide, placeholders } = await html2pptx(htmlPath, pptx, { tmpDir: path.join(__dirname, 'tmp') });

        // 第 13 页：柱状图填充 placeholder
        if (file === '13-chart.html' && placeholders.length > 0) {
            slide.addChart(pptx.charts.BAR, [{
                name: '占位数据',
                labels: ['类别一', '类别二', '类别三', '类别四'],
                values: [3, 5, 4, 6]
            }], {
                ...placeholders[0],
                barDir: 'col',
                showTitle: false,
                showLegend: false,
                showValue: true,
                dataLabelPosition: 'outEnd',
                dataLabelColor: '1F2937',
                showCatAxisTitle: true,
                catAxisTitle: '类别占位',
                catAxisTitleColor: '6B7280',
                catAxisLabelColor: '1F2937',
                showValAxisTitle: true,
                valAxisTitle: '数值占位',
                valAxisTitleColor: '6B7280',
                valAxisLabelColor: '1F2937',
                valAxisMinVal: 0,
                valAxisMaxVal: 8,
                valAxisMajorUnit: 2,
                chartColors: ['1B4332']
            });
        }
        console.log(`Converted: ${file}`);
    }

    const out = path.join(__dirname, '高中化学课件模板.pptx');
    await pptx.writeFile({ fileName: out });
    console.log('Presentation created:', out);
}

createPresentation().catch((err) => {
    console.error(err);
    process.exit(1);
});
