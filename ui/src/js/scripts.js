// 新增数据观察系统
class EntityObserver {
    static proxyMap = new WeakMap();

    static observe(data, callback) {
        return new Proxy(data, {
            set(target, key, value) {
                const old = target[key];
                target[key] = value;
                callback(key, old, value);
                return true;
            }
        });
    }
}

// 新增实体基类
class GameEntity {
    constructor(data) {
        this.id = data.id;
        this.type = data.type;
        this._data = EntityObserver.observe(data, this._onDataChange.bind(this));
    }

    _onDataChange(key, oldVal, newVal) {
        const element = document.querySelector(`[data-entity-id="${this.id}"]`);
        if (element) this.updateElement(element, key, newVal);
    }

    updateElement(element, key, value) {
        // 将在子类中具体实现
    }
}

class EntityFactory {
    static create(type, data) {
        const entityClass = {
            player: PlayerEntity,
            treasure: TreasureEntity,
        }[type];

        if (!entityClass) throw new Error(`未知实体类型: ${type}`);
        return new entityClass(data);
    }
}

class PlayerEntity extends GameEntity {
    updateElement(element, key, value) {
        switch (key) {
            case 'health':
                element.querySelector('.health').textContent = value;
                break;
            case 'attack':
                const attackEl = element.querySelector('.attack');
                if (attackEl) attackEl.textContent = value;
                break;
            case 'mana':
                this._updateMana(element, value);
                break;
        }
    }

    _updateMana(element, manaData) {
        const manaContainer = element.querySelector('.mana-column');
        manaContainer.innerHTML = Object.entries(manaData)
            .map(([type, val]) => `<div class="mana ${type.toLowerCase()}">${val}</div>`)
            .join('');
    }

    get template() {
        return `
            <div class="player-container" data-entity-id="${this.id}">
                <div class="player-name">${this._data.name}</div>
                <div class="avatar ${this._data.part === 1 ? 'enemy' : 'ally'}-avatar">
                    <div class="stats">
                        ${this._data.attack > 0 ? `<div class="attack">${this._data.attack}</div>` : ''}
                        <div class="health">${this._data.health}</div>
                    </div>
                </div>
                <div class="mana-column">
                    ${Object.entries(this._data.mana)
            .map(([type, val]) => `<div class="mana ${type.toLowerCase()}">${val}</div>`)
            .join('')}
                </div>
            </div>
        `;
    }
}

class TreasureEntity extends GameEntity {
    updateElement(element, key, value) {
        switch (key) {
            case 'health':
                element.querySelector('.health').textContent = value;
                break;
            case 'attack':
                element.querySelector('.attack').textContent = value;
                break;
        }
    }

    get template() {
        return `
            <div class="minion-card treasure" data-entity-id="${this.id}">
                <div class="stats">
                    <div class="attack">${this._data.attack}</div>
                    <div class="health">${this._data.health}</div>
                </div>
                <div class="card-name">${this._data.name}</div>
                <div class="treasure-icon"></div>
            </div>
        `;
    }
}

// 继续添加其他实体类型...


class BattleManager {
    static state = {
        players: new Map(),
        entities: new Map(),
        currentTurn: 0
    };

    static async init() {
        try {
            const response = await fetch('log.json');
            const battleData = await response.json();

            battleData.forEach((event, index) => {
                setTimeout(() => this.processEvent(event), index * 1000);
            });
        } catch (error) {
            console.error('战斗数据加载失败:', error);
        }
    }

    static processEvent(event) {
        this.updateLog(event);
        switch (event.type) {
            case 'add_player':
                this._handlePlayer(event.player);
                break;
            case 'play_card':
                this._handleCard(event.card);
                break;
            case 'attack':
                this.highlightCombatants(event.attacker_id, event.defender_id);
                break;
            case 'deal_damage':
                this.applyDamage(event);
                break;
            case 'destroy':
                this.handleDestruction(event);
                break;
            case 'new_turn':
                this.handleTurnChange(event);
                break;
        }
    }
 static _handlePlayer(playerData) {
        const entity = EntityFactory.create('player', playerData);
        const container = this._createEntityContainer(entity, playerData.part);
        this.entities.set(playerData.id, entity);

        const targetArea = document.querySelector(
            playerData.part === 1 ? '.row-1 .player-area' : '.row-4 .player-area'
        );
        targetArea.innerHTML = container;
    }

     static _handleCard(cardData) {
        const type = cardData.type === 'treasure' ? 'treasure' : 'minion';
        const entity = EntityFactory.create(type, cardData);
        const container = this._createEntityContainer(entity, cardData.owner_id);
        this.entities.set(cardData.id, entity);

        const targetArea = document.querySelector(
            cardData.owner_id === 1 ? '.row-2' : '.row-3'
        );
        targetArea.insertAdjacentHTML('beforeend', container);
    }    static _createEntityContainer(entity, ownerId) {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = entity.template;

        // 动态绑定事件
        const element = wrapper.firstElementChild;
        element.addEventListener('click', () => this._onEntityClick(entity));
        element.addEventListener('mouseover', () => this._onEntityHover(entity));

        return wrapper.innerHTML;
    }

    static _onEntityClick(entity) {
        // 处理点击逻辑
        console.log('Entity clicked:', entity);
    }

    static _onEntityHover(entity) {
        // 处理悬停逻辑
        CardPreview.show(entity._data);
    }
    static highlightCombatants(attackerId, defenderId) {
        const addTempClass = (element, className) => {
            element?.classList.add(className);
            setTimeout(() => element?.classList.remove(className), 500);
        };

        addTempClass(document.querySelector(`[data-id="${attackerId}"]`), 'attacking');
        addTempClass(document.querySelector(`[data-id="${defenderId}"]`), 'defending');
    }

    static applyDamage(event) {
        const entity = this.entities.get(event.defender_id);
        if (!entity) return;

        // 直接修改数据，观察系统会自动更新DOM
        entity._data.health -= event.damage;

        // 保留动画效果
        const element = document.querySelector(`[data-entity-id="${entity.id}"]`);
        element.classList.add('damaged');
        setTimeout(() => element.classList.remove('damaged'), 500);
    }

    static updateLog(logEntry) {
        const logArea = document.getElementById('log-area');
        const logElement = document.createElement('div');
        logElement.className = 'log-entry';
        logElement.textContent = `[回合 ${logEntry.turn || 0}] ${logEntry.log}`;
        logArea.appendChild(logElement);
        logArea.scrollTop = logArea.scrollHeight;
    }

    static handleDestruction(event) {
        const target = event.d_type === 'player' ?
            this.state.players.get(event.id) :
            this.state.entities.get(event.id);

        if (!target) return;

        if (event.d_type === 'player') {
            target.element.style.filter = 'grayscale(100%)';
            target.element.style.opacity = '0.5';
            this.state.players.delete(event.id);
        } else {
            target.element.remove();
            this.state.entities.delete(event.id);
        }
    }

    static handleTurnChange(currentPlayerId) {
        // 玩家切换逻辑
        document.querySelectorAll('.avatar').forEach(avatar => {
            avatar.classList.toggle('active-turn',
                avatar.dataset.id === currentPlayerId.toString()
            );
        });
    }

    // 新增工具方法
    static createNamePlate = (playerData) => {
        const namePlate = document.createElement('div');
        namePlate.className = 'player-name';
        namePlate.textContent = playerData.name;
        return namePlate;
    }

    static createManaColumn = (playerData) => {
        const manaColumn = document.createElement('div');
        manaColumn.className = 'mana-column';
        Object.entries(playerData.mana).forEach(([type, value]) => {
            const mana = document.createElement('div');
            mana.className = `mana ${type.toLowerCase()}`;
            mana.textContent = value;
            manaColumn.appendChild(mana);
        });
        return manaColumn;
    }
}

window.onload = BattleManager.init.bind(BattleManager);
