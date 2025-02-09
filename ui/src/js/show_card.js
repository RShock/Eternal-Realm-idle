class CardPreview {
    static init() {
        this.previewImage = document.getElementById('card-preview-image');
        this.previewInfo = document.getElementById('card-preview-info');
        
        // 改为事件委托处理动态元素
        document.querySelectorAll('.cards-row').forEach(row => {
            row.addEventListener('mouseover', e => this.handleHover(e, true));
            row.addEventListener('mouseout', e => this.handleHover(e, false));
            row.addEventListener('click', e => this.handleClick(e));
        });
    }

    static handleHover(e, isEnter) {
        const card = e.target.closest('.minion-card');
        if (!card) return;
        
        isEnter ? this.show(card.dataset.card) : this.hide();
    }

    static handleClick(e) {
        const card = e.target.closest('.minion-card');
        if (card) this.show(card.dataset.card);
    }

 static show(entityData) {
        this.previewImage.src = entityData.image || '';
        this.previewImage.style.display = entityData.image ? 'block' : 'none';
        this.previewInfo.innerHTML = `
            <strong>${entityData.name}</strong><br>
            攻击: ${entityData.attack}<br>
            生命: ${entityData.health}
        `;
    }

    static hide() {
        this.previewImage.style.display = 'none';
        this.previewInfo.innerHTML = '';
    }
}

document.addEventListener('DOMContentLoaded', () => CardPreview.init());
