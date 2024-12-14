from flask import redirect, Blueprint

bp = Blueprint('redirects', __name__)

@bp.route('/skincare/steps-for-a-skincare-routine')
def a():
    return redirect('/skincare/steps-for-a-skincare-routine-2025', code=301)

@bp.route('/hair/how-to-take-care-of-high-porosity-hair')
def b():
    return redirect('/hair/how-to-take-care-of-high-porosity-hair-in-2025', code=301)

@bp.route('/hair/how-to-take-care-of-low-porosity-hair')
def c():
    return redirect('/hair/how-to-take-care-of-low-porosity-hair-in-2025', code=301)

@bp.route('/skincare/spearmint-tea-for-treating-acne')
def d():
    return redirect('/skincare/spearmint-natural-acne-remedies-in-2025', code=301)

@bp.route('/hair/vitamins-for-hair-growth')
def e():
    return redirect('/hair/vitamins-for-hair-growth-2025', code=301)

@bp.route('/skincare/how-to-tighten-your-skin')
def e():
    return redirect('/skincare/how-to-tighten-your-skin-2025', code=301)

@bp.route('/skincare/Lorem Ipsum')
def e():
    return redirect('/', code=301)

