import json,boto3,pandas as pd
from datetime import datetime
from io import StringIO

s3=boto3.client('s3')

SOURCE_BUCKET_NAME='raw-flightsdata-bucket'
BUCKET_NAME='transformed-flightsdata-bucket'



def lambda_handler(event, context):
    try:
        current_date=datetime.now().strftime("%Y-%m-%d")
        print(current_date)


        response=s3.get_object(Bucket=SOURCE_BUCKET_NAME,Key=f'date={current_date}/data.json')
        raw_data = response['Body'].read().decode('utf-8')
        flights_data = json.loads(raw_data)
        # print(flights_data)

        df=pd.DataFrame(columns = ['flight_date', 'departure_airport', 'departure_iata', 'departure_delay','departure_scheduled',\
                                    'departure_actual', 'arrival_airport', 'arrival_iata', 'arrival_delay', 'arrival_scheduled',\
                                    'arrival_actual','flight_number', 'flight_iata'])

        for item in flights_data:
            flight_date=item['flight_date']
            departure_airport=item['departure']['airport']
            departure_iata=item['departure']['iata']
            departure_delay=item['departure']['delay']
            departure_scheduled=item['departure']['scheduled']
            departure_actual=item['departure']['actual']
            arrival_airport=item['arrival']['airport']
            arrival_iata=item['arrival']['iata']
            arrival_delay=item['arrival']['delay']
            arrival_scheduled=item['arrival']['scheduled']
            arrival_actual=item['arrival']['actual']
            flight_number=item['flight']['number']
            flight_iata=item['flight']['iata']

            new_row=pd.DataFrame({ 'flight_date' : [flight_date],
            'departure_airport' : [departure_airport],
            'departure_iata' : [departure_iata],
            'departure_delay' : [departure_delay],
            'departure_scheduled' : [departure_scheduled],
            'departure_actual' : [departure_actual],
            
            'arrival_airport' : [arrival_airport],
            'arrival_iata' : [arrival_iata],
            'arrival_delay' : [arrival_delay],
            'arrival_scheduled' : [arrival_scheduled],
            'arrival_actual' : [arrival_actual],
            
            'flight_number' : [flight_number],
            'flight_iata' : [flight_iata]})

            df=pd.concat([df,new_row],ignore_index=True)

        df['departure_delay'] = pd.to_numeric(df['departure_delay'], errors='coerce').fillna(0).astype(int)
        df['arrival_delay'] = pd.to_numeric(df['arrival_delay'], errors='coerce').fillna(0).astype(int)

        
        df['flight_date'] = pd.to_datetime(df['flight_date'])
        df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'])
        df['arrival_scheduled'] = pd.to_datetime(df['arrival_scheduled'])
        
        df['departure_actual'] = pd.to_datetime(df['departure_actual'])
        df['arrival_actual'] = pd.to_datetime(df['arrival_actual'])
        
        df['flight_number'] = df['flight_number'].fillna(0).astype(int)
        
        
        df['year'] = df['flight_date'].dt.year
        df['month'] = df['flight_date'].dt.month
        df['day'] = df['flight_date'].dt.day

        
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s3_key=f'date={current_date}/transformed_data_{current_time}.csv'

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )



        return {
            'statusCode': 200,
            'body': f"Data for {current_date} has been loaded into {BUCKET_NAME}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

