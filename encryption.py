import tenseal as ts

def setup_fhe():
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = 2**40
    context.generate_galois_keys()
    context.generate_relin_keys()
    return context

def encrypt_vote(vote, context):
    encrypted_vote = ts.ckks_vector(context, [float(vote)])
    return encrypted_vote.serialize()

def decrypt_vote(ciphertext, context):
    encrypted_vote = ts.ckks_vector_from(context, ciphertext)
    decrypted_vote = encrypted_vote.decrypt()
    return round(decrypted_vote[0])

def add_encrypted_votes(encrypted_votes, context):
    total = ts.ckks_vector_from(context, encrypted_votes[0])
    for i in range(1, len(encrypted_votes)):
        total += ts.ckks_vector_from(context, encrypted_votes[i])
    return total.serialize()
