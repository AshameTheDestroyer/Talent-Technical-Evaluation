export type Pagination<T> = {
    count: number;
    total: number;
    data: Array<T>;
};