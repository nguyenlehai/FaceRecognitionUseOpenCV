USE [SHOP]
GO

/****** Object:  StoredProcedure [dbo].[invoiceHeader_GetList_ByCMTND]    Script Date: 4/6/2018 9:56:45 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[invoiceHeader_GetList_ByCMTND] @CMTND BIGINT
AS
    BEGIN
        SET NOCOUNT ON;
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        DECLARE @NewLineChar AS CHAR(2) = CHAR(13) + CHAR(10);

        SELECT  h.invoice_header_id ,
                h.invoice_code ,
                c.customer_name ,
                h.date ,
                h.total_money ,
                STUFF( (SELECT  'Item: ' + i.item_name + ' - Employee: '
                                + e.employee_name + ' - Money: '
                                + CAST(i.money AS NVARCHAR(30)) + '; '
                                + @NewLineChar
                        FROM    dbo.INVOICE_DETAIL d ,
                                dbo.ITEM i ,
                                dbo.EMPLOYEE e
                        WHERE   h.invoice_header_id = d.invoice_header_id
                                AND d.item_id = i.item_id
                                AND i.employee_id = e.employee_id
                        ORDER BY i.item_id
                FOR   XML PATH('') ,
                          TYPE).value('.', 'nvarchar(max)'), 1, 0, '') item_list
        FROM    dbo.INVOICE_HEADER h ,
                dbo.CUSTOMER c
        WHERE   h.customer_id = c.customer_id
                AND c.cmtnd = @CMTND
        ORDER BY h.date DESC;
    END;


GO


