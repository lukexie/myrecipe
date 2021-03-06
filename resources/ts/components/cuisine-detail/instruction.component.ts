import { Component, Input } from '@angular/core';

declare var require: any;

/**
 * 調理手順コンポーネント
 */
@Component({
    selector: '[instructions]',
    template: require('./instruction.component.html'),
})
export class InstructionComponent {
    @Input() items: any[];

    addRow() {
        this.items.push({});
    }

    deleteRow() {
        this.items.pop();
    }

    getOrder(_item: any) {
        if (!_item.sort_order) {
            _item.sort_order = this.items.length;
        }
        return `${_item.sort_order}：`;
    }
}
