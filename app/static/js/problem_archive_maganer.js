class ProblemPost {
    constructor(json) {
        this.hashed_id = json.hashed_id;
        this.name = json.name;
        this.statement = json.statement;
        this.solution = json.solution;
    }
    get getLink() {
        return `/archive/problem/${this.hashed_id}`
    }
    buildDOM() {
        container = document.createElement("a");
        container.href = this.getLink;
        container.innerHTML = this.name;
        return container;
    }
}


class dataProcessor {
    constructor() {
        ;
    }

    sort(query, objects) {
        parameter = query.parameter;
        increase = query.increase;
        if (increase) return objects.sort((a, b) => a.greaterThan(b, parameter));
        else return objects.sort((a, b) => b.greaterThan(a, parameter));
    }
    filter(query, objects) {
        parameter = query.parameter;
        return objects.filter(object => object.fits(parameter));
    }
}


class dataManager {
    constructor() {
        this.url = '/api/archive';
        this.objects = [];
        this.dataProcessor = new dataProcessor();
    }

    clear() {
        this.objects = [];
    }
    append(json) {
        this.objects.append(new ProblemPost(json));
    }
    fetch(type) {
        this.objects = this.fetchPostData({type: type});
    }
    sort(query) {
        return this.dataProcessor.sort(query, this.objects);
    }
    filter(query) {
        return this.dataProcessor.filter(query, this.objects);
    }

    async fetchPostData(query) {
        response = await fetch(this.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(query)
        });
        return await response.json();
    }
}

class domManager {
    constructor() {
        ;
    }
    buildObject(object) {
        return object.buildDOM();
    }
    buildObjects(objects) {
        return objects.map(this.buildObject);
    }
}


class archiveManager {
    constructor() {
        this.dataManager = new dataManager();
        this.domManager = new domManager();
    }
}