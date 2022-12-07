from sales.models import Transaction

def get_new_ref(base_code = None):
    if base_code is None:
        transaction = Transaction.objects.all().order_by('-date').first()
        if not transaction:
            return 'RF' + str(1).zfill(4)
        ref_num = int(str(transaction.reference).strip().replace('RF', ''))
        ref_num = ref_num + 1
        code = 'RF' + str(ref_num).zfill(4)
        if len(Transaction.objects.filter(reference = code)) == 0:
            return code
        return get_new_ref(ref_num)
    base_code = base_code + 1
    code = 'RF' + str(base_code).zfill(4)
    if len(Transaction.objects.filter(reference = code)) == 0:
        return code
    return get_new_ref(base_code)
