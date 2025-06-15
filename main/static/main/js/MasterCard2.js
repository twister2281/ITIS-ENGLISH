
class Node {
    constructor(value) {
        this.value = value;
        this.next = null;
        this.prev = null;
    }
}

class Deque {
    constructor() {
        this.front = null;
        this.rear = null;
        this.size = 0;
    }

    addFront(value) {
        const newNode = new Node(value);
        if (this.isEmpty()) {
            this.front = newNode;
            this.rear = newNode;
        } else {
            newNode.next = this.front;
            this.front.prev = newNode;
            this.front = newNode;
        }
        this.size++;
    }

    addBack(value) {
        const newNode = new Node(value);
        if (this.isEmpty()) {
            this.front = newNode;
            this.rear = newNode;
        } else {
            newNode.prev = this.rear;
            this.rear.next = newNode;
            this.rear = newNode;
        }
        this.size++;
    }

    removeFront() {
        if (this.isEmpty()) return null;
        const value = this.front.value;
        this.front = this.front.next;
        if (this.front) {
            this.front.prev = null;
        } else {
            this.rear = null;
        }
        this.size--;
        return value;
    }

    removeBack() {
        if (this.isEmpty()) return null;
        const value = this.rear.value;
        this.rear = this.rear.prev;
        if (this.rear) {
            this.rear.next = null;
        } else {
            this.front = null;
        }
        this.size--;
        return value;
    }

    peekFront() {
        return this.front?.value ?? null;
    }

    peekBack() {
        return this.rear?.value ?? null;
    }

    isEmpty() {
        return this.size === 0;
    }

    getSize() {
        console.log(this.size);
        return this.size;
    }
}

class Card {
    constructor(word, translation, id) {
        this.word = word;
        this.translation = translation;
        this.id = id;
    }
};


class MasterCard {
    buffer = new Deque(); // buffer следующих карт должен быть деком
    min_buffer_size = 5;
    token = '';
    add_url = '';

    constructor(token, add_url) {
        this.token = token;
        this.add_url = add_url;
    }

    go_to_next_card() {
        this.add_to_buffer();
        this.buffer.removeFront();
    }

    get_current_index() {
        return 1;
    }

    async get_current_card() {
        await this.add_to_buffer();

        return this.buffer.peekFront();
    }

    // пополнить buffer
    add_to_buffer() {
        return new Promise((resolve, reject) => {
            if (this.buffer.getSize() >= this.min_buffer_size) {
                resolve();
                return;
            }

            $.get(this.add_url, {}, function (data) {
                data.cards_buffer.forEach(card => {
                    this.buffer.addBack(new Card(card.word, card.translation, card.id));
                });
                resolve();
            }.bind(this));
        });
    }

    get_new_card_from_dict() {
        // GET REQUEST о получении новой карточки
    }

    remove_card(url, card_id) {
        $.post(url, {
            csrfmiddlewaretoken: this.token,
            card_id: card_id
        }, function (data) {
            console.log(data);
        }).fail(function (xhr, status, error) {
            alert('Произошла ошибка удаления: ' + error);
        });
    }

    remember_card(url) {
        $.post(url, {
            csrfmiddlewaretoken: this.token,
            card_id: this.buffer.peekFront().id
        }, function (data) {
            console.log(data);
        }).fail(function (xhr, status, error) {
            if (xhr.status === 400) {
                alert('Карточка с таким словом уже существует');
            } else {
                alert('Произошла ошибка в пометке помню карту: ' + error);
            }
        });
    }

    edit_card(url, word, translation) {
        return new Promise((resolve, reject) => {
            $.post(url, {
                csrfmiddlewaretoken: this.token,
                word: word,
                translation: translation,
                card_id: this.buffer.peekFront().id
            }, function(data) {
                this.buffer.removeFront();
                data.cards_buffer.forEach(card => {
                    this.buffer.addFront(new Card(card.word, card.translation, card.id));
                });
                resolve();
            }.bind(this)).fail(function(xhr, status, error) {
                if (xhr.status === 400) {
                    alert('Карточка с таким словом уже существует');
                } else {
                    alert('Произошла ошибка: ' + error);
                }
                reject(error);
            });
        });
    }

    dont_remember_card(url) {
        $.post(url, {
            csrfmiddlewaretoken: this.token,
            card_id: this.buffer.peekFront().id
        }, function (data) {
            console.log(data);
        }).fail(function (xhr, status, error) {
            if (xhr.status === 400) {
                alert('Карточка с таким словом уже существует');
            } else {
                alert('Произошла ошибка в пометке непомню карту: ' + error);
            }
        });
    }

    add_new_card(url, word, translation) {
        return new Promise((resolve, reject) => {
            $.post(url, {
                csrfmiddlewaretoken: this.token,
                word: word,
                translation: translation
            }, function(data) {
                data.cards_buffer.forEach(card => {
                    this.buffer.addFront(new Card(card.word, card.translation, card.id));
                });
                resolve();
            }.bind(this)).fail(function(xhr, status, error) {
                if (xhr.status === 400) {
                    alert('Карточка с таким словом уже существует');
                } else {
                    alert('Произошла ошибка: ' + error);
                }
                reject(error);
            });
        });
    }
}