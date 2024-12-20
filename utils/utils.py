def formata_preco(valor):
    return f'R${valor:.2f}'.replace('.', ',')


def cart_total_qtd(cart):
    return sum([item['amount'] for item in cart.values()])


def cart_totals(cart):
    return sum([
        item.get('quantitative_promotional_price')
        if item.get('quantitative_promotional_price')
        else item.get('quantitative_price') 
        for item in cart.values()  
    ])


def previous_page(num):
    return num - 1


def next_page(num):
    return num + 1