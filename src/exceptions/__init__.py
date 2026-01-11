import os,sys

#create class to define argument exception
class CustomException(Exception):
    def __init__(self, error_message:Exception,error_detail:sys):#to capture error message and to capture error detail
        self.error_message = CustomException 
        pass
        
    
    try:
        pass
    except Exception as e:
        raise CustomException(e,sys)
    
    @staticmethod
    def get_detail_error_message(error_message:Exeption,error_detail:sys)->str:
        _,_, exce_tb = error_detail.exc_info() #a,b,c =1,2,3 here we want to access only vaue of c so we skip the value of a & b by typing _ in here

        exception_block_line_namber = exce_tb.tb_frame.f_lineno#f_lineno--> using this because we are running code in try:(tryblock) line by line
        try_block_line_number = exce_tb.tb_lineno#these two lines deg=fines that how we are calculation tryblock & exception block and storing in working directory
        file_name = exce_tb.tb_frame.f_code.co_filename#in file_name variable exception try block . frame by frame means line by line . folder by folder and file by file executing try exception in main folder(src)
        
        #in which way we want to collect the message it will show error in this format
        error_message = f"""
        Error occurred in execution of:
        [{file_name}] at
        try block line number :[{try_block_line_number}]
        and exception block line number :[{exception_block_line_namber}]
        error message :[{error_message}]
        """
        return error_message

    def __str__(self):
        return self.error_message
    def __repr__(self):
        return CustomException.__name__.str()
        
        #tb  --> (try:) try block
        #exce_tb --> exception try block
        #f_lineno --> exception block line number
        #tb_lineno --> try block line number

        