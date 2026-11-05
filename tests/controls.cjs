const assert = require('node:assert/strict');

// Exercise the visible picker; native selects are only Radix's FormData bridge.
async function selectTrigger(control) {
  return await control.getAttribute('role') === 'combobox'
    ? control : control.locator('xpath=preceding-sibling::*[@role="combobox"][1]');
}

async function openSelect(control) {
  const trigger = await selectTrigger(control);
  if (!await trigger.isVisible() && (await trigger.getAttribute('id'))?.startsWith('filter-'))
    await control.page().getByRole('button', { name: '篩選任務', exact: true }).click();
  const owningDialog = await trigger.evaluate(el => el.closest('dialog')?.id);
  await trigger.click();
  const popup = control.page().getByRole('listbox');
  await popup.waitFor();
  const colors = await popup.evaluate(el => ({
    bg: getComputedStyle(el).backgroundColor, color: getComputedStyle(el).color,
    dialog: el.closest('dialog')?.id,
  }));
  assert.equal(colors.bg, 'rgb(32, 30, 27)');
  assert.equal(colors.color, 'rgb(233, 226, 212)');
  assert.equal(colors.dialog, owningDialog);
  return { trigger, popup };
}

async function selectValue(control, value) {
  const { popup } = await openSelect(control);
  await popup.locator('[role="option"][data-value=' + JSON.stringify(value) + ']').click();
  await popup.waitFor({ state: 'hidden' });
}

async function optionValues(control) {
  const { trigger, popup } = await openSelect(control);
  const values = await popup.getByRole('option').evaluateAll(items => items.map(el => el.dataset.value));
  await popup.press('Escape');
  await popup.waitFor({ state: 'hidden' });
  return values;
}

async function selectProject(page, id) {
  const button = page.locator('[data-project-id="' + id + '"]');
  await button.click();
  await page.waitForFunction(id => document.querySelector('[data-project-id="'+id+'"]')?.getAttribute('aria-current') === 'page', id);
}

module.exports = { selectProject, selectTrigger, openSelect, selectValue, optionValues };
