const tabs = document.querySelectorAll('[data-tab-value]');
const tabInfos = document.querySelectorAll('[data-tab-info]');
const buttons = document.getElementsByClassName('button');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = document
            .querySelector(tab.dataset.tabValue);

        tabInfos.forEach(tabInfo => {
            tabInfo.classList.remove('active');
        });
        target.classList.add('active');
    });
});

for (const button of buttons) {
    button.addEventListener('click', () => {
        if (!button.classList.contains('active')) {
            for (const tempButton of buttons) {
                if (tempButton.classList.contains('active')) {
                    tempButton.classList.remove('active');
                }
            }
            button.classList.add('active');
        }
    });
}
