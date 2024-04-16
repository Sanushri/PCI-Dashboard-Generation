pip install matplotlib
pip install pandas

import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import plotly.express as px
from io import StringIO

def main():
    st.set_page_config(page_title="PCI Dashboard",layout='wide', initial_sidebar_state='expanded')
    # CSS styling
    st.markdown("""
<style>
                [data-testid="stSidebar"] {
    background-image: url(https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png);
    background-size: 200px;
    background-repeat: no-repeat;
    background-position: 4px 20px;
}


/* Card */
/* Adapted from https://startbootstrap.com/theme/sb-admin-2 */
div.css-1r6slb0.e1tzin5v2 {
background-color: #FFFFFF;
border: 1px solid #CCCCCC;
padding: 5% 5% 5% 10%;
border-radius: 5px;

border-left: 0.5rem solid #9AD8E1 !important;
box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;

}

label.css-mkogse.e16fv1kl2 {
color: #36b9cc !important;
font-weight: 1000 !important;
text-transform: uppercase !important;
}


/* Move block container higher */
div.block-container.css-18e3th9.egzxvld2 {
margin-top: -5em;
}


/* Hide hamburger menu and footer */
div.css-r698ls.e8zbici2 {
display: none;
}

footer.css-ipbk5a.egzxvld4 {
display: none;
}

footer.css-12gp8ed.eknhn3m4 {
display: none;
}

div.vg-tooltip-element {
display: none;
}

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #404040;
    text-align: center;
    font-weight: bold;
    padding: 15px 0;
    border-left: 0.5rem solid #45818e !important;
    border-right: 0.5rem solid #45818e !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 1000;

                
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
    
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

    # with open('style.css') as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    #alt.themes.enable("dark")
    st.markdown('### PCI Dashboard Generator')

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df.head()
        st.write('Data Uploaded Successfully')
        st.write('All the Comparisons are done on Before Coupon and Convenience Fee Prices and w.r.t. Yatra')
        # with st.sidebar:
        #     st.title('Filters')
        #     year_list = list(df['City'].unique())   
        #     selected_city = st.selectbox('Select a city', year_list, index=len(year_list)-1)
        #     df_selected_city = df[df['City'] == selected_city]
        #     df_selected_city_sorted = df_selected_city.sort_values(by="City", ascending=False)
        
        df['Makemytripcth Base Rate']= df['Makemytripcth Base Rate'].replace('-',np.nan)
        df['Yatracw Base Rate']= df['Yatracw Base Rate'].replace('-',np.nan)
        df['Makemytripcth Hotel Offer']=df['Makemytripcth Hotel Offer'].replace('-',np.nan)
        df['Yatracw Hotel Offer']=df['Yatracw Hotel Offer'].replace('-',np.nan)
        df['Variance With Makemytripcth']=df['Variance With Makemytripcth'].replace('-',np.nan)
        


        df['Pre-OTA Hotel Price YT']=df['Yatracw Base Rate']-df['Yatracw Hotel Offer']
        df['Pre-OTA Hotel Price MMT']=df['Makemytripcth Base Rate']-df['Makemytripcth Hotel Offer']
        df['Pre-OTA vs Pre-OTA']=df['Pre-OTA Hotel Price YT']-df['Pre-OTA Hotel Price MMT']

        
        df.head()
        set1=df[df['Check_In_Date']==df['Check_In_Date'].iat[0]]
        set2=df[df['Check_In_Date']==df['Check_In_Date'].iat[1]]
        

        value_counts = df['Summary-PostCoupon'].apply(lambda x: 'Expensive' if x == "Expensive"  else ('RF' if x == "RF" else ('Beaten On Inventory' if x == "Beaten On Inventory" else 'At Par'))).value_counts(dropna=False)

        # Display the counts for each type, including NaN values
        print("Expensive Count:", value_counts.get('Expensive', 0))
        print("RF Count:", value_counts.get('RF', 0))
        print("Beaten On Inventory Count:", value_counts.get('Beaten On Inventory', 0))
        print("At Par Count:", value_counts.get('At Par', 0))
        print("Total Data Corpus:",len(df['UniqueNumber'])-1)
        length=len(df['UniqueNumber'])-1
        ex=value_counts.get('Expensive', 0)
        rf=value_counts.get('RF', 0)
        bi=value_counts.get('Beaten On Inventory', 0)
        par=value_counts.get('Beaten On Inventory', 0)
        # Row A
        st.markdown('### Overall Key Metrics')
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Total Expensive",value_counts.get('Expensive', 0),str(round((ex/length)*100,2))+"%")
        col2.metric("Total Request Failure",value_counts.get('RF', 0),str(round((rf/length)*100,2))+"%")
        col3.metric("Total Beaten On Inventory", value_counts.get('Beaten On Inventory', 0),str(round((bi/length)*100,2))+"%")
        col4.metric("Total Price At Par Cases",value_counts.get('Beaten On Inventory', 0),str(round((par/length)*100,2))+"%")
        col5.metric("Total number of Cases",length,str(100)+"%")

        st.write('Exploratory Data Analytics for',df['Check_In_Date'].iat[0], 'date set:')

        c1, c2, c3 = st.columns(3)
        with c1:
           
            value_counts = set1['Pre-OTA vs Pre-OTA'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else ('Zero' if x == 0 else 'NaN'))).value_counts(dropna=False)

            higher = value_counts.get('Positive',0)
            lower = value_counts.get('Negative',0)
            same=value_counts.get('Zero',0)
            NoneValue=value_counts.get('NaN',0)
            total=higher+lower+same+NoneValue
            higher=round((higher/total)*100,2)
            lower=round((lower/total)*100,2)
            same=round((same/total)*100,2)
            NoneValue=round((NoneValue/total)*100,2)

            #plotting chart
            labels = ['Higher', 'Lower', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [higher, lower, same,NoneValue]  # Replace with your actual counts
            fig=plt.figure(figsize=(6,4.8))
            plt.bar(labels, counts, color=['#995559', '#f35b53', '#ffae3a','#ff580f'])


            for index, value in enumerate(counts):
                plt.text(index, value, str(value)+"%", ha='center', va='bottom')
            #plt.figure(facecolor='black')
            #plt.xlabel('Hotel Promo vs Hotel Promo')
            plt.ylabel('Count')
            plt.title('Comparison of Pre-OTA Coupon Excluding GST price')
            st.pyplot(fig)

        with c2:
            # Assuming df['Base vs Base'] contains the price differences between the two websites
            value_counts = set1['Base vs Base'].apply(lambda x: 'Expensive' if x > 0 else ('Cheaper' if x < 0 else ('Same' if x == 0 else 'NaN'))).value_counts(dropna=False)
            # Extract counts for each category
            Expensive = value_counts.get('Expensive', 0)
            Cheaper = value_counts.get('Cheaper', 0)
            Same = value_counts.get('Same', 0)
            NoneValue=value_counts.get('NaN',0)

            # Plotting chart
            labels = ['Expensive', 'Cheaper', 'Same','Av Exclv./RF/\nClosed on\nBoth/\nBeaten Inventory']
            counts = [Expensive, Cheaper, Same,NoneValue]  # Replace with your actual counts
            colors = ['#995559', '#f35b53', '#ffae3a','#ff580f']
            plt.title('Comparison of Base Rates',fontsize=6)
            fig=plt.figure(figsize=(4, 3.9))
            plt.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=95 , textprops={'fontsize': 7})
            plt.xlabel('Base Rate vs Base Rate' , fontsize = 6)
            plt.figure(facecolor='black')
            
            plt.axis('equal')
            st.pyplot(fig)
        with c3:
            value_counts = set1['HotelPromo vs HotelPromo'].apply(lambda x: 'Expensive' if x > 0 else ('Cheaper' if x < 0 else ('Same' if x == 0 else 'NaN'))).value_counts(dropna=False)
            # Extract counts for each category
            Expensive = value_counts.get('Expensive', 0)
            Cheaper = value_counts.get('Cheaper', 0)
            Same = value_counts.get('Same', 0)
            NoneValue=value_counts.get('NaN',0)
            total=Expensive+Cheaper+Same+NoneValue
            Expensive=round((Expensive/total)*100,2)
            Cheaper=round((Cheaper/total)*100,2)
            Same=round((Same/total)*100,2)
            NoneValue=round((NoneValue/total)*100,2)


            labels = ['Expensive', 'Cheaper', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [Expensive, Cheaper, Same,NoneValue]  # Replace with your actual counts
            colors = ['#995559', '#f35b53', '#ffae3a','#ff580f']
            ds=pd.DataFrame({"Labels": labels,"Values": counts})
            rslt_ds = ds.sort_values(by = 'Values', ascending = False)
            print(rslt_ds) 
            fig=plt.figure(figsize=(4, 4.5))
            # Plotting chart
            plt.fill_betweenx(y=[1,3.8],x1=[8,10],x2=[6,4],color=colors[0])
            plt.fill_betweenx(y=[4,6.8],x1=[10,12],x2=[4,2],color=colors[1])
            plt.fill_betweenx(y=[7,9.8],x1=[12,14],x2=[2,0],color=colors[2])
            plt.fill_betweenx(y=[10,12.8],x1=[14,16],x2=[0,-2],color=colors[3])
            plt.xticks([],[])
            plt.yticks([2,5,8,11],rslt_ds['Labels'][::-1])
            #plt.xlabel("Comparison")
            for y , value in zip([2,5,8,11],rslt_ds['Values'][::-1]):
                plt.text(7,y,str(value)+"%",fontsize=11,color="black",ha="center")
            plt.title('Comparison of Hotel Promo Prices',loc="center")
            st.pyplot(fig)
        
        c1, c2 , c3= st.columns(3)
        with c1:
            value_counts = set1['Variance With Makemytripcth'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else ('Zero' if x == 0 else 'NaN'))).value_counts(dropna=False)

            # Display the counts for each type including NaN Values
            print("Positive Count:", value_counts.get('Positive', 0))
            print("Negative Count:", value_counts.get('Negative', 0))
            print("Zero Count:", value_counts.get('Zero', 0))
            print("NaN Count:", value_counts.get('NaN', 0))

            higher = value_counts.get('Positive',0)
            lower = value_counts.get('Negative',0)
            same=value_counts.get('Zero',0)
            NoneValue=value_counts.get('NaN',0)
            #plotting chart
            labels = ['Higher', 'Lower', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [higher, lower, same, NoneValue]  # Replace with your actual counts
            fig=plt.figure(figsize=(3,3))
            plt.barh(labels, counts, color=['#995559', '#f35b53', '#ffae3a','#ff580f'])

            # for index, value in enumerate(counts):
            #     plt.text(index, value, str(value), ha='center', va='bottom')
                #   Set the fontsize for x-axis ticks
            plt.xticks(fontsize=6)
            plt.yticks(fontsize=6) 

            plt.xlabel('')
            #plt.ylabel('Count')
            plt.title('Comparison of Final Prices',fontsize=6)
            st.pyplot(fig)
        
        with c2:
            value_counts = set1['Summary-Before Coupon & ConvFee'].apply(lambda x: 'At Par' if x == 'At Par' else ('Beaten On Inventory' if x == 'Beaten On Inventory' else ('At Par' if x == 'Expensive' else ('Available Exclusive' if x == 'Available Exclusive' else('RF' if x == 'RF' else 'NaN' ))))).value_counts(dropna=False)

            Par = value_counts.get('At Par',0)
            Beaten = value_counts.get('Beaten On Inventory',0)
            Excl =value_counts.get('Available Exclusive',0)
            RFc =value_counts.get('RF',0)
            total=Par+Beaten+Excl+RFc
            Par=round((Par/total)*100,2)
            Beaten=round((Beaten/total)*100,2)
            Excl=round((Excl/total)*100,2)
            RFc=round((RFc/total)*100,2)

            #plotting chart
            labels = ['At Par', 'Beaten On \n Inventory', 'Available Exclusive','RF']
            counts = [Par, Beaten, Excl,RFc]  # Replace with your actual counts
            fig=plt.figure(figsize=(6,5.5))
            plt.bar(labels, counts, color=['#995559', '#f35b53', '#ffae3a','#ff580f'])


            for index, value in enumerate(counts):
                plt.text(index, value, str(value)+"%", ha='center', va='bottom')
            #plt.figure(facecolor='black')
            #plt.xlabel('Hotel Promo vs Hotel Promo')
            plt.ylabel('Count')
            plt.title('Inventory Summary')
            st.pyplot(fig)
        with c3:
            mmt=[]
            yt=[]
            value_counts = set1['Yatracw MealPlan'].apply(lambda x: 'Absent' if x == '-' else 'Present').value_counts(dropna=False)
            Abs = value_counts.get('Absent',0)
            Pre = value_counts.get('Present',0)
            total=Abs+Pre
            Abs=round((Abs/total)*100,2)
            Pre=round((Pre/total)*100,2)
            yt.append(Abs)
            yt.append(Pre)

            value_counts = set1['Makemytripcth MealPlan'].apply(lambda x: 'Absent' if x == '-' else 'Present').value_counts(dropna=False)
            absent=value_counts.get('Absent',0)
            present=value_counts.get('Present',0)
            Total=absent+present
            absent=round((absent/Total)*100,2)
            present=round((present/Total)*100,2)

            mmt.append(absent)
            mmt.append(present)

            # create data 
            p = np.arange(2) 
           
            width = 0.2
            fig=plt.figure(figsize=(6,5.5))
  
            # plot data in grouped manner of bar type 
            bar1=plt.bar(p, yt, width, color='orange') 
            bar2=plt.bar(p+0.2, mmt, width, color='#ff580f') 
             
            plt.xticks(p, ['Without Inclusion', 'With Inclusion']) 
            plt.xlabel("Meal Plan") 
            plt.ylabel("Count") 
            plt.legend(["Yatra", "MMT"]) 
            plt.title('Meal Inclusions Summary')
            for bar1, bar2 in zip(bar1, bar2):
             yval1 = bar1.get_height()
             yval2 = bar2.get_height()
             plt.text(bar1.get_x() + bar1.get_width()/2.0, yval1 + 1, f"{yval1}"+"%", ha='center', va='bottom')
             plt.text(bar2.get_x() + bar2.get_width()/2.0, yval2 + 1, f"{yval2}"+"%", ha='center', va='bottom')

            st.pyplot(fig) 

        
        st.write('Exploratory Data Analytics for',df['Check_In_Date'].iat[1], 'date set:')
        c1, c2, c3 = st.columns(3)
        with c1:
            # df1=df[df['Summary-Before Coupon & ConvFee'].isin(constraint)]
            value_counts = set2['Pre-OTA vs Pre-OTA'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else ('Zero' if x == 0 else 'NaN'))).value_counts(dropna=False)

            higher = value_counts.get('Positive',0)
            lower = value_counts.get('Negative',0)
            same=value_counts.get('Zero',0)
            NoneValue=value_counts.get('NaN',0)
            total=higher+lower+same+NoneValue
            higher=round((higher/total)*100,2)
            lower=round((lower/total)*100,2)
            same=round((same/total)*100,2)
            NoneValue=round((NoneValue/total)*100,2)
            #plotting chart
            labels = ['Higher', 'Lower', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [higher, lower, same,NoneValue]  # Replace with your actual counts
            fig=plt.figure(figsize=(6,4.8))
            plt.bar(labels, counts, color=['#4b0082', '#8a2be2', '#8e4585','#3d85c6'])


            for index, value in enumerate(counts):
                plt.text(index, value, str(value)+"%", ha='center', va='bottom')
            #plt.figure(facecolor='black')
            # plt.xlabel('Hotel Promo vs Hotel Promo')
            plt.ylabel('Count')
            plt.title('Comparison of Pre-OTA Coupon price')
            st.pyplot(fig)

        with c2:
            # Assuming df['Base vs Base'] contains the price differences between the two websites
            value_counts = set2['Base vs Base'].apply(lambda x: 'Expensive' if x > 0 else ('Cheaper' if x < 0 else ('Same' if x == 0 else 'NaN'))).value_counts(dropna=False)
            # Extract counts for each category
            Expensive = value_counts.get('Expensive', 0)
            Cheaper = value_counts.get('Cheaper', 0)
            Same = value_counts.get('Same', 0)
            NoneValue=value_counts.get('NaN',0)

            # Plotting chart
            labels = ['Expensive', 'Cheaper', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [Expensive, Cheaper, Same,NoneValue]  # Replace with your actual counts
            colors = ['#4b0082', '#8a2be2', '#8e4585','#3d85c6']

            fig=plt.figure(figsize=(4, 3.9))
            plt.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=95 , textprops={'fontsize': 7})
            plt.xlabel('Base Rate vs Base Rate' , fontsize = 6)
            plt.figure(facecolor='black')
            plt.title('Comparison of Base Prices')
            plt.axis('equal')
            st.pyplot(fig)
        with c3:
            value_counts = set2['HotelPromo vs HotelPromo'].apply(lambda x: 'Expensive' if x > 0 else ('Cheaper' if x < 0 else ('Same' if x == 0 else 'NaN'))).value_counts(dropna=False)
            # Extract counts for each category
            Expensive = value_counts.get('Expensive', 0)
            Cheaper = value_counts.get('Cheaper', 0)
            Same = value_counts.get('Same', 0)
            NoneValue=value_counts.get('NaN',0)
            total=Expensive+Cheaper+Same+NoneValue
            Expensive=round((Expensive/total)*100,2)
            Cheaper=round((Cheaper/total)*100,2)
            Same=round((Same/total)*100,2)
            NoneValue=round((NoneValue/total)*100,2)

            labels = ['Expensive', 'Cheaper', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [Expensive, Cheaper, Same,NoneValue]  # Replace with your actual counts
            colors = ['#4b0082', '#8a2be2', '#8e4585','#3d85c6']
            ds=pd.DataFrame({"Labels": labels,"Values": counts})
            rslt_ds = ds.sort_values(by = 'Values', ascending = False)
            print(rslt_ds) 
            fig=plt.figure(figsize=(4, 4.5))
            # Plotting chart
            plt.fill_betweenx(y=[1,3.8],x1=[8,10],x2=[6,4],color=colors[0])
            plt.fill_betweenx(y=[4,6.8],x1=[10,12],x2=[4,2],color=colors[1])
            plt.fill_betweenx(y=[7,9.8],x1=[12,14],x2=[2,0],color=colors[2])
            plt.fill_betweenx(y=[10,12.8],x1=[14,16],x2=[0,-2],color=colors[3])
            plt.xticks([],[])
            plt.yticks([2,5,8,11],rslt_ds['Labels'][::-1])
            plt.xlabel("Comparison")
            for y , value in zip([2,5,8,11],rslt_ds['Values'][::-1]):
                plt.text(7,y,str(value)+"%",fontsize=11,color="white",ha="center")
            plt.title('Comparison of Hotel Offer Prices',loc="center")
            st.pyplot(fig)
        
        c1, c2 ,c3= st.columns(3)
        with c1:
            value_counts = set2['Variance With Makemytripcth'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else ('Zero' if x == 0 else 'NaN'))).value_counts(dropna=False)

            # Display the counts for each type including NaN Values
            print("Positive Count:", value_counts.get('Positive', 0))
            print("Negative Count:", value_counts.get('Negative', 0))
            print("Zero Count:", value_counts.get('Zero', 0))
            print("NaN Count:", value_counts.get('NaN', 0))

            higher = value_counts.get('Positive',0)
            lower = value_counts.get('Negative',0)
            same=value_counts.get('Zero',0)
            NoneValue=value_counts.get('NaN',0)
            #plotting chart
            labels = ['Higher', 'Lower', 'Same','Av Exclv./RF/\nClosed on Both/\nBeaten Inventory']
            counts = [higher, lower, same, NoneValue]  # Replace with your actual counts
            fig=plt.figure(figsize=(3,3))
            plt.barh(labels, counts, color=['#4b0082', '#8a2be2', '#8e4585','#3d85c6'])

            # for index, value in enumerate(counts):
            #     plt.text(index, value, str(value), ha='center', va='bottom')
            plt.xticks(fontsize=6)  # Set the fontsize for x-axis ticks
            plt.yticks(fontsize=6) 

            plt.xlabel('')
            #plt.ylabel('Count')
            plt.title('Comparison of Final Prices',fontsize=6)
            st.pyplot(fig)
        with c2:
            value_counts = set2['Summary-Before Coupon & ConvFee'].apply(lambda x: 'At Par' if x == 'At Par' else ('Beaten On Inventory' if x == 'Beaten On Inventory' else ('At Par' if x == 'Expensive' else ('Available Exclusive' if x == 'Available Exclusive' else('RF' if x == 'RF' else 'NaN' ))))).value_counts(dropna=False)

            Par = value_counts.get('At Par',0)
            Beaten = value_counts.get('Beaten On Inventory',0)
            Excl =value_counts.get('Available Exclusive',0)
            RFc =value_counts.get('RF',0)
            total=Par+Beaten+Excl+RFc
            Par=round((Par/total)*100,2)
            Beaten=round((Beaten/total)*100,2)
            Excl=round((Excl/total)*100,2)
            RFc=round((RFc/total)*100,2)
            

            #plotting chart
            labels = ['At Par', 'Beaten On \n Inventory', 'Available Exclusive','RF']
            counts = [Par, Beaten, Excl,RFc]  # Replace with your actual counts
            fig=plt.figure(figsize=(6,5.5))
            plt.bar(labels, counts, color=['#4b0082', '#8a2be2', '#8e4585','#3d85c6'])


            for index, value in enumerate(counts):
                plt.text(index, value, str(value)+"%", ha='center', va='bottom')
            #plt.figure(facecolor='black')
            #plt.xlabel('Hotel Promo vs Hotel Promo')
            plt.ylabel('Count')
            plt.title('Inventory Summary')
            st.pyplot(fig)
        with c3:
            mmt=[]
            yt=[]
            value_counts = set2['Yatracw MealPlan'].apply(lambda x: 'Absent' if x == '-' else 'Present').value_counts(dropna=False)
            Abs = value_counts.get('Absent',0)
            Pre = value_counts.get('Present',0)
            total=Abs+Pre
            Abs=round((Abs/total)*100,2)
            Pre=round((Pre/total)*100,2)
            yt.append(Abs)
            yt.append(Pre)

            value_counts = set1['Makemytripcth MealPlan'].apply(lambda x: 'Absent' if x == '-' else 'Present').value_counts(dropna=False)
            absent=value_counts.get('Absent',0)
            present=value_counts.get('Present',0)
            Total=absent+present
            absent=round((absent/Total)*100,2)
            present=round((present/Total)*100,2)
            mmt.append(absent)
            mmt.append(present)

            # create data 
            p = np.arange(2) 
           
            width = 0.2
            fig=plt.figure(figsize=(6,5.5))
  
            # plot data in grouped manner of bar type 
            bar1=plt.bar(p, yt, width, color='orange') 
            bar2=plt.bar(p+0.2, mmt, width, color='pink') 
             
            plt.xticks(p, ['Without Inclusion', 'With Inclusion']) 
            plt.xlabel("Meal Plan") 
            plt.ylabel("Count") 
            plt.legend(["Yatra", "MMT"]) 
            plt.title('Meal Inclusions Summary')
            for bar1, bar2 in zip(bar1, bar2):
             yval1 = bar1.get_height()
             yval2 = bar2.get_height()
             plt.text(bar1.get_x() + bar1.get_width()/2.0, yval1 + 1, f"{yval1}"+"%", ha='center', va='bottom')
             plt.text(bar2.get_x() + bar2.get_width()/2.0, yval2 + 1, f"{yval2}"+"%", ha='center', va='bottom')


            st.pyplot(fig) 
            



    
if __name__=="__main__":
    main()
    
