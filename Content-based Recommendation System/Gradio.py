import pandas as pd
import numpy as np
import gradio as gr
# to deal with images
from PIL import Image
import urllib.request


# Load data and models
def load_models():
    global main_feature4m_df, cosine_sim
    main_feature4m_df = pd.read_csv('cleaned_data_v5.csv')
    cosine_sim = np.load('cosine_sim11.npy')

load_models()

def content_based_recommendations(product_id: int, data: pd.DataFrame, cosine_sim: np.ndarray, n: int = 5):
    """
    Generate content-based recommendations based on product_id.
    
    Parameters:
    - product_id: The ID of the product to base recommendations on.
    - data: DataFrame containing the product data.
    - cosine_sim: Precomputed cosine similarity matrix.
    - n: Number of recommendations to generate.
    
    Returns:
    - A tuple of DataFrame with recommended products and their similarity scores.
    """
    try:
        idx = data[data['product_id'] == product_id].index[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Product ID not found")
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    product_indices = [i[0] for i in sim_scores]
    
    # return a list of recommended product_id, product_name, rating, rating_count, discounted_price, actual_price, category_1, category_2, img_link_y
    return data.iloc[product_indices][['product_id', 'product_name', 'rating', 'rating_count', 'discounted_price', 'actual_price', 'category_1', 'category_2', 'img_link_y', 'sale_rate']], sim_scores


def api_home():
    """
    Home endpoint to check API status.
    """
    return {'detail': 'Welcome to FastAPI TextGen Tutorial!'}


def get_recommendations(product_id: int, num_recommendations: int = 5):
    """
    Generate product recommendations based on the provided product ID.
    
    Parameters:
    - request: RecommendationRequest object containing product_id and num_recommendations.
    
    Returns:
    - JSON response with recommended product IDs and their similarity scores.
    """
    recommendations, sim_scores = content_based_recommendations(
        product_id, main_feature4m_df, cosine_sim, num_recommendations
    )
    return {
        'product_id': product_id,
        'recommendations': recommendations.to_dict(orient='records'),
        'similarity_scores': sim_scores
    }


def get_best_selling(n: int = 3):
    """
    Get the best selling products.
    
    Parameters:
    - n: Number of best selling products to return.
    
    Returns:
    - JSON response with best selling products.
    """
    best_selling = main_feature4m_df.sort_values('rating_count', ascending=False).head(n)
    return best_selling.to_dict(orient='records')


def get_new_arrivals(n: int = 5):
    """
    Get the new arrivals.
    
    Parameters:
    - n: Number of new arrivals to return.
    
    Returns:
    - JSON response with new arrival products.
    """
    most_sale_rate = main_feature4m_df.sort_values('sale_rate', ascending=False).head(n)
    return most_sale_rate.to_dict(orient='records')

# function for gradio takes the recomended json and returns the product_name and img_link_y

def get_recommendations_gr(input_id):
    recomms, _ = content_based_recommendations(
        input_id, main_feature4m_df, cosine_sim, 6
    )
    return recomms[['product_name', 'img_link_y']]


def get_recommendations_names_gr():
    products_names = get_recommendations_gr()['product_name'].tolist()
    product_name_1 = products_names[0]
    product_name_2 = products_names[1]
    product_name_3 = products_names[2]
    product_name_4 = products_names[3]
    product_name_5 = products_names[4]
    product_name_6 = products_names[5]
    return product_name_1, product_name_2, product_name_3, product_name_4, product_name_5, product_name_6

def get_recommendations_images_gr(input_id):
    products_images = get_recommendations_gr(input_id)['img_link_y'].tolist()

    # read the image from the link
    urllib.request.urlretrieve(products_images[0], 'product_image_1.jpg')
    urllib.request.urlretrieve(products_images[1], 'product_image_2.jpg')
    urllib.request.urlretrieve(products_images[2], 'product_image_3.jpg')
    urllib.request.urlretrieve(products_images[3], 'product_image_4.jpg')
    urllib.request.urlretrieve(products_images[4], 'product_image_5.jpg')
    urllib.request.urlretrieve(products_images[5], 'product_image_6.jpg')
    # for original image
    urllib.request.urlretrieve(main_feature4m_df[main_feature4m_df['product_id'] == input_id]['img_link_y'].values[0], 'product_image_0.jpg')

    product_image_1 = Image.open('product_image_1.jpg')
    product_image_2 = Image.open('product_image_2.jpg')
    product_image_3 = Image.open('product_image_3.jpg')
    product_image_4 = Image.open('product_image_4.jpg')
    product_image_5 = Image.open('product_image_5.jpg')
    product_image_6 = Image.open('product_image_6.jpg')
    product_image_0 = Image.open('product_image_0.jpg')
    return product_image_1, product_image_2, product_image_3, product_image_4, product_image_5, product_image_6, product_image_0



with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown('# ')
        with gr.Row(variant='panel'):
            with gr.Column(scale=1):
                input_id = gr.Number(22, label='Product ID for Examples: [22, 27, 76, 92, 117]', minimum= 20, maximum= 2000, step=1)
                run_btn = gr.Button('Generate', variant='primary', interactive=True)
            with gr.Column(scale=1):
                processed_image = gr.Image(type='pil', label="Product", interactive=False, height=320, width= 320, image_mode='RGBA', elem_id="disp_image")
                with gr.Row():
                    view_1 = gr.Image(interactive=False, height=240, width=240, label="Recommendation 1")
                    view_2 = gr.Image(interactive=False, height=240, width=240, label="Recommendation 2")
                    view_3 = gr.Image(interactive=False, height=240, width=240, label="Recommendation 3")
                with gr.Row():
                    view_4 = gr.Image(interactive=False, height=240, width=240, label="Recommendation 4")
                    view_5 = gr.Image(interactive=False, height=240, width=240, label="Recommendation 5")
                    view_6 = gr.Image(interactive=False, height=240, width=240, label="Recommendation 6")
        

        run_btn.click(fn=get_recommendations_images_gr, 
                        inputs=[input_id], 
                        outputs=[view_1, view_2, view_3, view_4, view_5, view_6, processed_image], queue=True)
            # ).success(fn=partial(gen_multiview, pipeline, predictor), 
            #             inputs=[processed_image_highres, scale_slider, steps_slider, seed, output_processing],
            #             outputs=[view_1, view_2, view_3, view_4, view_5, view_6])
        
        demo.queue().launch(share=True, max_threads=80)
